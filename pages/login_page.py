"""Page Object de la pantalla de login de saucedemo.com."""

import logging

from selenium.webdriver.common.by import By

from pages.base_page import BasePage

logger = logging.getLogger(__name__)


class LoginPage(BasePage):
    CAMPO_USUARIO = (By.ID, "user-name")
    CAMPO_PASSWORD = (By.ID, "password")
    BOTON_LOGIN = (By.ID, "login-button")
    MENSAJE_ERROR = (By.CSS_SELECTOR, "[data-test='error']")

    def abrir_login(self):
        self.abrir()
        self.encontrar(self.CAMPO_USUARIO)
        return self

    def login(self, usuario, password):
        logger.info("Iniciando sesión con el usuario '%s'", usuario)
        self.escribir(self.CAMPO_USUARIO, usuario)
        self.escribir(self.CAMPO_PASSWORD, password)
        self.click(self.BOTON_LOGIN)

    def esta_cargada(self):
        """Espera a que el formulario de login esté visible (lanza TimeoutException si no)."""
        self.encontrar(self.BOTON_LOGIN)
        return self.esta_visible(self.CAMPO_USUARIO)

    def obtener_mensaje_error(self):
        return self.obtener_texto(self.MENSAJE_ERROR)
