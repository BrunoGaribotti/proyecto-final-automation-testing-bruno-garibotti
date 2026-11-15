"""Casos de prueba del carrito de compras."""

import pytest

from pages.cart_page import CartPage
from utils.helpers import login


@pytest.mark.ui
def test_agregar_producto_al_carrito(driver):
    inventario = login(driver)

    nombre_producto = inventario.agregar_producto_por_indice(0)
    assert inventario.cantidad_en_carrito() == 1, "El contador del carrito no cambió a 1"

    inventario.ir_al_carrito()
    assert CartPage(driver).obtener_nombres_items() == [nombre_producto]


@pytest.mark.ui
def test_agregar_varios_productos_al_carrito(driver):
    inventario = login(driver)

    nombres = [inventario.agregar_producto_por_indice(i) for i in range(3)]
    assert inventario.cantidad_en_carrito() == 3

    inventario.ir_al_carrito()
    assert sorted(CartPage(driver).obtener_nombres_items()) == sorted(nombres)
