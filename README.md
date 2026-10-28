# 🏦 Sistema Bancario - Refactoring, Testing e Integración Continua

Proyecto integrador para las asignaturas **Refactoring y Testing** e **Integración y Entrega Continua**.

## 👥 Integrantes y Equipo de Desarrollo
* **Mara Vanesa San Martín** (Tests de Dominio, Tests de Integración DAO, CI/CD)
* **Daniel Ricardo González** 
* **Erika Muñoz** 
* **Cristian Testaseca**
* **Andrés Verdún** 
* **Romina Marín** 
* **Valentina San Martín** 

## 🎯 Objetivos del Proyecto
* **Refactoring & Código Limpio:** Aplicación de principios SOLID (SRP, OCP, LSP, ISP, DIP), eliminación de Code Smells y lectura tipo periódico (*Extract Method*).
* **Testing Automatizado:** Suite integral unitaria y de integración usando `pytest` con arquitectura Arrange-Act-Assert (AAA) y fixtures.
* **Persistencia Desacoplada:** Manejo de DAO (Data Access Object) mediante SQLAlchemy ORM y SQLite (con soporte en memoria para tests).
* **Integración Continua (CI/CD):** Pipeline automatizado con **GitHub Actions** que ejecuta la suite de pruebas tras cada `push` y `Pull Request`.

## 🏛️ Arquitectura y Principios SOLID
1. **Single Responsibility Principle (SRP):** Desacoplamiento total entre la Lógica de Negocio (`src/cliente.py`, `src/cuenta.py`, etc.), la Persistencia (`src/dao.py`, `src/models.py`) y la Presentación (`app_banco.py`).
2. **Liskov Substitution Principle (LSP):** La clase `CuentaAhorro` extiende de `Cuenta` respetando estrictamente los contratos y comportamiento de la clase base.
3. **Inversión de Dependencias & DAO:** Uso de `DAO(":memory:")` para aislar completamente las pruebas de integración sin afectar la base de datos de producción.

## 🧪 Pruebas Automatizadas (`pytest`)

El proyecto cuenta con una suite completa dividida en dos niveles:

### 1. Tests Unitarios (Dominio de Negocio)
* `tests/test_cliente.py`: Validaciones de formato, datos requeridos e integridad de `Cliente`.
* `tests/test_cuenta.py`: Depósitos, retiros, control de saldo y excepción `SaldoInsuficienteError`.
* `tests/test_transaccion.py`: Historial de operaciones y marcas de tiempo (`datetime`).
* `tests/test_cuenta_ahorro.py`: Cálculo de tasas de interés y validación de herencia LSP.
* `tests/test_tarjeta.py`: Compras, pagos y control de cupo con `LimiteExcedidoError`.

### 2. Tests de Integración (Persistencia & DAO)
* `tests/test_dao.py`: Verificación de operaciones CRUD, claves foráneas y mapeo ORM SQLite mediante base de datos en memoria (`:memory:`).

## 🚀 Instalación y Ejecución Local

1. Clonar el repositorio
```bash
git clone [https://github.com/mevaktecno-vane/sistema_bancario.git](https://github.com/mevaktecno-vane/sistema_bancario.git)
cd sistema_bancario

2. Crear y activar el Entorno Virtual (venv)
PowerShell
# En Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1

# En Linux/macOS
python3 -m venv venv
source venv/bin/activate

3. Instalar dependencias
Bash
pip install -r requirements.txt

4. Ejecutar la suite de pruebas
Bash
# Correr todos los tests unitarios e integrativos
pytest

# Correr con reporte detallado de cobertura
pytest --cov=src -v

5. Ejecutar la Aplicación
Bash
# Interfaz gráfica principal (Flet)
python main.py

## 🐳 Ejecutar con Docker

Requiere Docker Desktop con el motor Linux activo. Desde la raíz del proyecto:

```bash
docker compose up --build
```

Abrir [http://localhost:8550](http://localhost:8550). Para detener la aplicación,
usar `Ctrl+C`; para iniciarla en segundo plano, ejecutar
`docker compose up --build -d` y detenerla con `docker compose down`.

La imagen incluye una copia de `sistema_bancario.db`. Al primer inicio, esa copia
se carga en el volumen persistente `bank_data`; los siguientes inicios conservan
los datos del volumen y no vuelven a sobrescribirlos. Para eliminar también la
base persistente y comenzar de cero, ejecutar `docker compose down -v`.

La ruta de la base se puede cambiar mediante `BANK_DB_PATH`. No usar una base con
datos sensibles reales en una imagen compartida o publicada.

⚙️ Integración Continua (CI/CD)
El repositorio cuenta con un workflow de GitHub Actions configurado en .github/workflows/ci.yml. En cada push a cualquier rama o apertura de Pull Request, el servidor de CI:
1.	Configura el entorno Python aislado.
2.	Instala las dependencias del requirements.txt.
3.	Ejecuta la suite completa de pytest asegurando que no se introduzcan regresiones a main.
