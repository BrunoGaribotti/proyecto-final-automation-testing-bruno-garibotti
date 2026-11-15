"""Configuración compartida de pytest.

- Fixture `driver`: abre un Chrome nuevo por test (tests independientes) y lo cierra al final.
- Hook `pytest_runtest_makereport`: si un test de UI falla, guarda una captura en
  reports/screenshots/ con fecha/hora y nombre del test, y la adjunta al reporte HTML.
"""

import base64
import logging
import os
from datetime import datetime
from pathlib import Path

import pytest
from selenium import webdriver

CARPETA_CAPTURAS = Path(__file__).resolve().parent / "reports" / "screenshots"

logger = logging.getLogger("framework")

# Selenium y urllib3 registran cada petición HTTP al driver: se silencian para que
# el log muestre sólo los pasos del framework.
for ruidoso in ("selenium", "urllib3"):
    logging.getLogger(ruidoso).setLevel(logging.WARNING)


def _crear_opciones_chrome():
    opciones = webdriver.ChromeOptions()
    # En CI (o con HEADLESS=1) se ejecuta sin ventana.
    if os.getenv("HEADLESS", "0") == "1" or os.getenv("CI"):
        opciones.add_argument("--headless=new")
    opciones.add_argument("--window-size=1366,900")
    opciones.add_argument("--no-sandbox")
    opciones.add_argument("--disable-dev-shm-usage")
    # Evita el popup de Chrome "contraseña filtrada", que tapa la página tras el login.
    opciones.add_argument("--disable-features=PasswordLeakDetection")
    opciones.add_experimental_option(
        "prefs",
        {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.password_manager_leak_detection": False,
        },
    )
    return opciones


@pytest.fixture
def driver(request):
    logger.info("Iniciando Chrome para el test: %s", request.node.name)
    navegador = webdriver.Chrome(options=_crear_opciones_chrome())
    navegador.implicitly_wait(0)
    yield navegador
    logger.info("Cerrando Chrome del test: %s", request.node.name)
    navegador.quit()


def _nombre_archivo_seguro(nombre):
    return "".join(c if c.isalnum() or c in "-_" else "_" for c in nombre)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    resultado = yield
    reporte = resultado.get_result()

    if reporte.when != "call" or not reporte.failed:
        return

    navegador = item.funcargs.get("driver") if hasattr(item, "funcargs") else None
    if navegador is None:
        # Test de API u otro test sin navegador: no hay captura que sacar.
        logger.error("Falló el test %s", item.nodeid)
        return

    CARPETA_CAPTURAS.mkdir(parents=True, exist_ok=True)
    marca_tiempo = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    ruta = CARPETA_CAPTURAS / f"{marca_tiempo}_{_nombre_archivo_seguro(item.name)}.png"

    try:
        png = navegador.get_screenshot_as_png()
    except Exception as error:  # el navegador pudo haberse cerrado
        logger.error("No se pudo tomar la captura de %s: %s", item.nodeid, error)
        return

    ruta.write_bytes(png)
    logger.error("Falló el test %s. Captura guardada en %s", item.nodeid, ruta)

    # Adjuntar la captura al reporte HTML (embebida, funciona con --self-contained-html).
    pytest_html = item.config.pluginmanager.getplugin("html")
    if pytest_html is not None:
        extras = getattr(reporte, "extras", [])
        extras.append(pytest_html.extras.image(base64.b64encode(png).decode(), mime_type="image/png"))
        extras.append(pytest_html.extras.text(str(ruta), name="Ruta de la captura"))
        reporte.extras = extras


def pytest_html_report_title(report):
    report.title = "Proyecto Final - Automation Testing (Bruno Garibotti)"
