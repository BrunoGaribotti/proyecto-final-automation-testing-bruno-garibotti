"""Clase base de la que heredan todos los Page Objects.

Centraliza las esperas explícitas y las acciones comunes (click, escribir,
leer texto) para que cada página sólo declare sus localizadores y acciones.
"""

import logging

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

BASE_URL = "https://www.saucedemo.com/"
TIEMPO_ESPERA = 10

logger = logging.getLogger(__name__)


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.espera = WebDriverWait(driver, TIEMPO_ESPERA)

    def abrir(self, ruta=""):
        url = BASE_URL + ruta
        logger.info("Abriendo URL: %s", url)
        self.driver.get(url)

    def encontrar(self, localizador):
        """Espera a que el elemento sea visible y lo devuelve."""
        return self.espera.until(EC.visibility_of_element_located(localizador))

    def encontrar_todos(self, localizador):
        return self.driver.find_elements(*localizador)

    def click(self, localizador):
        logger.info("Click en %s", localizador)
        self.espera.until(EC.element_to_be_clickable(localizador)).click()

    def escribir(self, localizador, texto):
        logger.info("Escribiendo '%s' en %s", texto, localizador)
        campo = self.encontrar(localizador)
        campo.clear()
        campo.send_keys(texto)

    def obtener_texto(self, localizador):
        return self.encontrar(localizador).text

    def esta_visible(self, localizador):
        elementos = self.driver.find_elements(*localizador)
        return len(elementos) > 0 and elementos[0].is_displayed()

    def url_actual(self):
        return self.driver.current_url

    def esperar_url(self, fragmento):
        self.espera.until(EC.url_contains(fragmento))
