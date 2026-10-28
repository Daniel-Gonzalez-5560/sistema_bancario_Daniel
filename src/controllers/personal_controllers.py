# src/controllers/personal_controller.py
from src.models.dao_personal import DAOPersonal
from src.controllers.sesion import Sesion
from src.controllers.navegacion import ir_a


class PersonalController:
    """Controlador mediador entre el DAOPersonal y la Vista de Personal."""

    def __init__(self, dao: DAOPersonal = None, view=None):
        self.dao = dao or DAOPersonal()
        self.view = view  # Referencia a la vista

    def validar_acceso(self) -> bool:
        """Verifica si el usuario en sesión tiene rol personal."""
        usuario = Sesion.actual()
        return usuario is not None and usuario.get("rol") == "personal"

    def cargar_datos_iniciales(self):
        """Carga clientes y sus cuentas desde el Modelo y le ordena a la Vista renderizarlos."""
        if not self.validar_acceso():
            self.view.redirigir_login()
            return

        try:
            clientes = self.dao.obtener_todos_clientes()
            # Mapeamos cada cliente junto a sus cuentas asociadas
            datos_tabla = []
            for id_cli, nom, ape, dni, categoria, estado in clientes:
                try:
                    cuentas = self.dao.obtener_cuentas_por_cliente(id_cli)
                except Exception:
                    cuentas = []
                datos_tabla.append({
                    "id": id_cli,
                    "nombre_completo": f"{nom} {ape}",
                    "dni": dni,
                    "cuentas": cuentas
                })

            self.view.actualizar_tabla(datos_tabla)
        except Exception as err:
            self.view.mostrar_alerta(f"Error al cargar clientes: {str(err)}", color="red")

    def registrar_nuevo_cliente(self, e):
        """Orquesta la navegación hacia el formulario de alta."""
        from src.views.home_crear_cliente import render_gestion_cliente
        self.view.navegar_a(render_gestion_cliente)

    def abrir_detalle_cliente(self, dni: str):
        """Orquesta la apertura del detalle/edición de un cliente."""
        from src.views.home_crear_cliente import render_gestion_cliente
        self.view.navegar_a(lambda p: render_gestion_cliente(p, dni=dni))

    def cerrar_sesion(self, e):
        """Cierra la sesión y redirige al login."""
        Sesion.cerrar()
        self.view.redirigir_login()