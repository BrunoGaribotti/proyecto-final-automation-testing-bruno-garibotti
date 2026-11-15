"""Funciones reutilizables entre tests de UI."""

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage

USUARIO_VALIDO = "standard_user"
PASSWORD_VALIDO = "secret_sauce"


def login(driver, usuario=USUARIO_VALIDO, password=PASSWORD_VALIDO):
    """Inicia sesión y devuelve la página de inventario ya cargada."""
    LoginPage(driver).abrir_login().login(usuario, password)
    inventario = InventoryPage(driver)
    inventario.esperar_url(InventoryPage.RUTA)
    return inventario
