# Proyecto Final - Automation Testing

Framework de automatización de pruebas en Python que combina **pruebas de UI** con Selenium WebDriver sobre [saucedemo.com](https://www.saucedemo.com/) y **pruebas de API** con Requests sobre [JSONPlaceholder](https://jsonplaceholder.typicode.com/). Genera un reporte HTML con capturas de pantalla de los fallos y un log detallado de cada ejecución.

Parte de la pre-entrega (login, inventario y carrito), reorganizada con el patrón **Page Object Model** y ampliada con checkout, ordenamiento, escenarios negativos, datos externos, pruebas de API, logging e integración continua.

## Propósito del proyecto

- Automatizar flujos completos de una tienda web: login, navegación del catálogo, ordenamiento, carrito y checkout.
- Validar una API REST pública: códigos de estado, estructura y contenido del JSON, escenarios de éxito y de error, y peticiones encadenadas.
- Dejar una base ordenada a la que se le puedan sumar pruebas nuevas fácilmente.

## Tecnologías utilizadas

| Herramienta | Uso |
|---|---|
| Python | Lenguaje principal |
| Pytest | Framework de testing (fixtures, parametrización, markers) |
| Selenium WebDriver | Automatización del navegador Google Chrome |
| Requests | Pruebas de API |
| pytest-html | Reporte HTML con capturas embebidas |
| logging | Registro de pasos en consola y en archivo |
| Git / GitHub | Control de versiones |
| GitHub Actions | Ejecución automática en cada push |

## Estructura del proyecto

```
proyecto-final-automation-testing-bruno-garibotti/
├── .github/workflows/
│   └── tests.yml            # Pipeline de CI: corre las pruebas y publica los reportes
├── data/
│   ├── login_data.csv       # Usuarios y resultados esperados del login
│   ├── checkout_data.json   # Compras y datos de comprador para el checkout
│   └── api_posts.json       # Posts a crear en las pruebas de API
├── pages/                   # Page Object Model
│   ├── base_page.py         # Esperas y acciones comunes
│   ├── login_page.py
│   ├── inventory_page.py
│   ├── cart_page.py
│   └── checkout_page.py
├── tests/
│   ├── ui/
│   │   ├── test_login.py     # Login parametrizado (positivos y negativos) y logout
│   │   ├── test_inventory.py # Catálogo y ordenamiento de productos
│   │   ├── test_cart.py      # Agregar uno o varios productos al carrito
│   │   └── test_checkout.py  # Compra completa y checkout con datos incompletos
│   └── api/
│       ├── conftest.py       # Fixture del cliente de API
│       └── test_posts_api.py # GET, POST, PUT, PATCH, DELETE y flujos encadenados
├── utils/
│   ├── api_client.py        # Envoltorio de Requests con logging
│   ├── data_loader.py       # Lectura de CSV y JSON
│   └── helpers.py           # Login reutilizable
├── reports/                 # Reporte HTML y capturas (se generan al ejecutar)
├── logs/                    # Log de la ejecución (se genera al ejecutar)
├── conftest.py              # Fixture del navegador y capturas automáticas en fallos
├── pytest.ini               # Configuración de pytest, reporte y logging
└── requirements.txt
```

## Cobertura de pruebas

**UI (saucedemo.com):**
- Login parametrizado desde CSV: 2 usuarios válidos y 4 escenarios negativos (usuario bloqueado, contraseña incorrecta, usuario vacío, contraseña vacía).
- Logout.
- El inventario muestra productos, logo, filtro y menú.
- Ordenamiento por nombre y por precio, en ambos sentidos.
- Agregar uno y varios productos al carrito.
- Checkout completo de punta a punta, parametrizado desde JSON.
- Checkout con datos incompletos (escenario negativo).

**API (JSONPlaceholder):**
- `GET` del listado, por id, con filtro, y de un recurso inexistente (404).
- `POST` parametrizado desde JSON, `PUT`, `PATCH` y `DELETE`.
- Flujos encadenados: post → autor → comentarios, y crear → actualizar → borrar.

Cada test abre su propio navegador (o su propio cliente de API), así que la falla de uno no afecta a los demás.

## Instalación de dependencias

Requisitos: Python 3.10 o superior y Google Chrome instalado.

```bash
git clone https://github.com/BrunoGaribotti/proyecto-final-automation-testing-bruno-garibotti.git
cd proyecto-final-automation-testing-bruno-garibotti
python -m venv .venv
.venv\Scripts\activate        # En Linux/Mac: source .venv/bin/activate
pip install -r requirements.txt
```

No hace falta descargar ChromeDriver: Selenium Manager lo resuelve automáticamente.

## Ejecución de las pruebas

```bash
pytest                    # todas las pruebas
pytest -m ui              # sólo UI
pytest -m api             # sólo API
pytest -m e2e             # sólo flujos de punta a punta
pytest tests/ui/test_login.py
```

Para ejecutar sin abrir la ventana del navegador:

```bash
set HEADLESS=1            # En Linux/Mac: export HEADLESS=1
pytest
```

## Cómo interpretar los reportes

- **`reports/reporte.html`**: abrilo en el navegador. Arriba muestra el resumen (cuántas pruebas pasaron, fallaron o se saltearon y la duración total) y abajo una fila por prueba con su estado y duración. Se puede filtrar por estado. Al desplegar una prueba fallida se ven el error, el log de ese test y la **captura de pantalla** del momento de la falla.
- **`reports/screenshots/`**: las capturas de los tests de UI que fallaron, nombradas `AAAA-MM-DD_HH-MM-SS_nombre_del_test.png`.
- **`logs/ejecucion.log`**: el detalle paso a paso de toda la ejecución (URL abiertas, clicks, datos ingresados, peticiones y respuestas de la API). Sirve para depurar un fallo.
- **GitHub Actions**: en cada push se ejecutan las pruebas. En la pestaña *Actions* del repositorio, cada ejecución publica el artefacto `reportes-de-pruebas` con el reporte, las capturas y el log para descargar.
