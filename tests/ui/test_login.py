"""Casos de prueba de login (positivos y negativos).

Los datos se leen de data/login_data.csv y cada fila genera un test independiente.
"""

import pytest

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from utils.data_loader import leer_csv
from utils.helpers import login

CASOS_LOGIN = leer_csv("login_data.csv")


@pytest.mark.ui
@pytest.mark.parametrize("caso", CASOS_LOGIN, ids=[c["caso"] for c in CASOS_LOGIN])
def test_login(driver, caso):
    login_page = LoginPage(driver).abrir_login()
    login_page.login(caso["usuario"], caso["password"])

    if caso["debe_funcionar"] == "true":
        inventario = InventoryPage(driver)
        assert inventario.esta_cargada(), "No se cargó la página de inventario tras el login"
        assert inventario.obtener_logo() == "Swag Labs"
    else:
        assert login_page.obtener_mensaje_error() == caso["mensaje_esperado"]
        assert "inventory.html" not in login_page.url_actual()


@pytest.mark.ui
def test_logout(driver):
    inventario = login(driver)
    inventario.logout()

    login_page = LoginPage(driver)
    assert login_page.esta_visible(LoginPage.BOTON_LOGIN), "No se volvió a la pantalla de login"
