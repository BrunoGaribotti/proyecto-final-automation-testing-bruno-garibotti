"""Casos de prueba del catálogo de productos (navegación y filtros)."""

import logging

import pytest

from utils.helpers import login

logger = logging.getLogger(__name__)


@pytest.mark.ui
def test_inventario_muestra_productos(driver):
    inventario = login(driver)

    assert inventario.esta_cargada()
    assert driver.title == "Swag Labs"
    assert inventario.obtener_logo() == "Swag Labs"

    productos = inventario.obtener_productos()
    assert len(productos) > 0, "No se muestran productos en el inventario"

    primero = inventario.obtener_datos_producto(0)
    logger.info("Primer producto: %s - %s", primero["nombre"], primero["precio"])
    assert primero["nombre"] != ""
    assert primero["precio"].startswith("$")

    assert inventario.filtro_visible(), "El filtro de ordenamiento no está visible"
    assert inventario.menu_visible(), "El botón del menú no está visible"


@pytest.mark.ui
@pytest.mark.parametrize(
    "opcion, clave, descendente",
    [
        ("Name (A to Z)", "nombre", False),
        ("Name (Z to A)", "nombre", True),
        ("Price (low to high)", "precio", False),
        ("Price (high to low)", "precio", True),
    ],
)
def test_ordenar_productos(driver, opcion, clave, descendente):
    inventario = login(driver)
    inventario.ordenar_por(opcion)

    valores = inventario.obtener_nombres() if clave == "nombre" else inventario.obtener_precios()
    assert valores == sorted(valores, reverse=descendente), f"Orden incorrecto con '{opcion}'"
