# src/views/home_personal.py
import flet as ft
from src.navegacion import ir_a
from src.sesion import Sesion
from src.controllers.personal_controllers import PersonalController

# Constantes de diseño - Capital Bank Desktop Neon
BG_FONDO = "#0c0b11"
BG_TABLA = "#121118"
BORDE_NEON = "#9333ea"
BORDE_NEON_BRIGHT = "#a855f7"
LINEA_DIVISORIA = "#232130"
COLOR_ENCABEZADO = "#7e7894"
COLOR_BLANCO = "#ffffff"


class HomePersonalView:
    def __init__(self, page: ft.Page, controller):
        self.page = page
        self.controller = controller
        self.controller.view = self  # Conexión bidireccional canónica

        # Contenedor dinámico donde se inyectan las filas reactivamente
        self.columna_filas = ft.Column(spacing=0, scroll=ft.ScrollMode.ADAPTIVE)

    def build_ui(self):
        """Configuración de página y ensamblado visual inicial."""
        self.page.title = "Capital Bank - Personal"
        self.page.window_width = 980
        self.page.window_height = 640
        self.page.window_resizable = True
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.page.bgcolor = BG_FONDO

        # ---- Encabezado: Logo y Título ----
        logo_widget = ft.Row(
            spacing=10,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Container(
                    width=46,
                    height=52,
                    border_radius=8,
                    border=ft.border.all(2, BORDE_NEON_BRIGHT),
                    shadow=ft.BoxShadow(blur_radius=12, color=BORDE_NEON, offset=ft.Offset(0, 0)),
                    alignment=ft.alignment.center,
                    content=ft.Column(
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=1,
                        controls=[
                            ft.Icon(ft.Icons.SHIELD_OUTLINED, color=BORDE_NEON_BRIGHT, size=24),
                            ft.Text("CB", size=9, weight=ft.FontWeight.BOLD, color=BORDE_NEON_BRIGHT),
                        ],
                    ),
                ),
                ft.Column(
                    spacing=0,
                    controls=[
                        ft.Text("CAPITAL", size=13, weight=ft.FontWeight.BOLD, color=COLOR_BLANCO),
                        ft.Text("BANK", size=13, weight=ft.FontWeight.BOLD, color=COLOR_BLANCO),
                    ],
                ),
            ],
        )

        header = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Row(
                    spacing=24,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        logo_widget,
                        ft.Column(
                            spacing=2,
                            controls=[
                                ft.Text("VISTA PERSONAL", size=11, weight=ft.FontWeight.BOLD, color=BORDE_NEON_BRIGHT),
                                ft.Text("Clientes", size=32, weight=ft.FontWeight.BOLD, color=COLOR_BLANCO),
                                ft.Text("Dale de alta a los clientes y a sus cuentas", size=13, color=COLOR_ENCABEZADO),
                            ],
                        ),
                    ],
                ),
                ft.Row(
                    spacing=12,
                    controls=[
                        ft.ElevatedButton(
                            content=ft.Text("+ Alta cliente", size=14, weight=ft.FontWeight.W_600, color=COLOR_BLANCO),
                            bgcolor=BORDE_NEON,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=10),
                                padding=ft.Padding(20, 14, 20, 14),
                                shadow_color=BORDE_NEON_BRIGHT,
                                elevation=6,
                            ),
                            # El clic se delega al controlador
                            on_click=self.controller.registrar_nuevo_cliente,
                        ),
                        ft.IconButton(
                            icon=ft.Icons.LOGOUT_ROUNDED,
                            icon_color=COLOR_ENCABEZADO,
                            icon_size=20,
                            tooltip="Cerrar sesión",
                            # El cierre se delega al controlador
                            on_click=self.controller.cerrar_sesion,
                        ),
                    ],
                ),
            ],
        )

        # ---- Tabla Header ----
        tabla_header = ft.Container(
            padding=ft.Padding(24, 16, 24, 12),
            content=ft.Row(
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Container(expand=3, content=ft.Text("CLIENTE", size=11, weight=ft.FontWeight.BOLD, color=COLOR_ENCABEZADO)),
                    ft.Container(expand=2, content=ft.Text("DNI", size=11, weight=ft.FontWeight.BOLD, color=COLOR_ENCABEZADO)),
                    ft.Container(expand=3, content=ft.Text("CUENTAS", size=11, weight=ft.FontWeight.BOLD, color=COLOR_ENCABEZADO)),
                    ft.Container(expand=1, alignment=ft.alignment.center_right, content=ft.Text("ACCIÓN", size=11, weight=ft.FontWeight.BOLD, color=COLOR_ENCABEZADO)),
                ],
            ),
        )

        tabla_contenedor = ft.Container(
            bgcolor=BG_TABLA,
            border_radius=18,
            border=ft.border.all(1.5, BORDE_NEON),
            shadow=ft.BoxShadow(blur_radius=18, color="#581c87", offset=ft.Offset(0, 0)),
            content=ft.Column(
                spacing=0,
                controls=[
                    tabla_header,
                    ft.Container(height=1, bgcolor=LINEA_DIVISORIA),
                    self.columna_filas,
                ],
            ),
        )

        self.page.clean()
        self.page.add(
            ft.Container(
                padding=ft.Padding(36, 28, 36, 28),
                expand=True,
                content=ft.Column(
                    expand=True,
                    spacing=24,
                    controls=[header, tabla_contenedor],
                ),
            )
        )

        # Solicita los datos al controlador para inicializar
        self.controller.cargar_datos_iniciales()

    def actualizar_tabla(self, clientes: list[dict]):
        """Renderiza reactivamente los datos enviados por el controlador."""
        self.columna_filas.controls.clear()

        if not clientes:
            self.columna_filas.controls.append(
                ft.Container(
                    padding=40,
                    alignment=ft.alignment.center,
                    content=ft.Text("No hay clientes registrados en el sistema.", size=13, color=COLOR_ENCABEZADO),
                )
            )
            self.page.update()
            return

        for cli in clientes:
            dni_actual = cli["dni"]
            fila = ft.Container(
                padding=ft.Padding(24, 14, 24, 14),
                border=ft.Border(bottom=ft.BorderSide(1, LINEA_DIVISORIA)),
                content=ft.Row(
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Container(expand=3, content=ft.Text(cli["nombre_completo"], size=14, weight=ft.FontWeight.W_500, color=COLOR_BLANCO)),
                        ft.Container(expand=2, content=ft.Text(str(cli["dni"]), size=14, color=COLOR_BLANCO)),
                        ft.Container(expand=3, content=ft.Row(wrap=True, spacing=6, controls=self._crear_badges_cuentas(cli["cuentas"]))),
                        ft.Container(
                            expand=1,
                            alignment=ft.alignment.center_right,
                            content=ft.OutlinedButton(
                                content=ft.Text("Ver", size=12, color=COLOR_BLANCO),
                                style=ft.ButtonStyle(
                                    side=ft.BorderSide(1, BORDE_NEON_BRIGHT),
                                    shape=ft.RoundedRectangleBorder(radius=10),
                                    padding=ft.Padding(18, 8, 18, 8),
                                ),
                                on_click=lambda e, d=dni_actual: self.controller.abrir_detalle_cliente(d),
                            ),
                        ),
                    ],
                ),
            )
            self.columna_filas.controls.append(fila)

        self.page.update()

    def _crear_badges_cuentas(self, cuentas):
        if not cuentas:
            return [ft.Text("Sin cuentas", size=11, color=COLOR_ENCABEZADO)]
        badges = []
        for c in cuentas:
            nombre = c.__class__.__name__.lower() if hasattr(c, "__class__") else str(c).lower()
            label = "Caja de ahorro" if "ahorro" in nombre else "Corriente"
            badges.append(
                ft.Container(
                    padding=ft.Padding(10, 4, 10, 4),
                    border=ft.border.all(1, BORDE_NEON_BRIGHT),
                    border_radius=8,
                    content=ft.Text(label, size=11, color=COLOR_BLANCO),
                )
            )
        return badges

    def redirigir_login(self):
        from src.login import render_login
        ir_a(self.page, render_login)

    def navegar_a(self, vista_destino):
        ir_a(self.page, vista_destino)

    def mostrar_alerta(self, mensaje: str, color: str = "green"):
        bg = ft.Colors.GREEN_700 if color == "green" else ft.Colors.RED_700
        self.page.overlay.append(ft.SnackBar(ft.Text(mensaje), open=True, bgcolor=bg))
        self.page.update()


# Función de entrada retrocompatible
def render_home_personal(page: ft.Page):
    controller = PersonalController()
    view = HomePersonalView(page, controller)
    view.build_ui()

