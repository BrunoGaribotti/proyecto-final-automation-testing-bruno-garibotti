"""Flujo completo de compra: login -> agregar productos -> carrito -> checkout.

Los productos y los datos del comprador se leen de data/checkout_data.json.
"""

import pytest

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from utils.data_loader import leer_json
from utils.helpers import login

DATOS = leer_json("checkout_data.json")


@pytest.mark.ui
@pytest.mark.e2e
@pytest.mark.parametrize("compra", DATOS["compras"], ids=[c["caso"] for c in DATOS["compras"]])
def test_checkout_completo(driver, compra):
    inventario = login(driver)
    for producto in compra["productos"]:
        inventario.agregar_producto_por_nombre(producto)

    inventario.ir_al_carrito()
    carrito = CartPage(driver)
    assert sorted(carrito.obtener_nombres_items()) == sorted(compra["productos"])
    carrito.ir_al_checkout()

    checkout = CheckoutPage(driver)
    comprador = compra["comprador"]
    checkout.completar_datos(comprador["nombre"], comprador["apellido"], comprador["codigo_postal"])

    assert sorted(checkout.obtener_items_resumen()) == sorted(compra["productos"])
    assert checkout.obtener_total().startswith("Total: $")

    checkout.finalizar_compra()
    assert checkout.obtener_mensaje_confirmacion() == "Thank you for your order!"


@pytest.mark.ui
@pytest.mark.parametrize(
    "datos", DATOS["datos_incompletos"], ids=[d["caso"] for d in DATOS["datos_incompletos"]]
)
def test_checkout_con_datos_incompletos(driver, datos):
    """Escenario negativo: el checkout no avanza si falta algún dato obligatorio."""
    inventario = login(driver)
    inventario.agregar_producto_por_indice(0)
    inventario.ir_al_carrito()
    CartPage(driver).ir_al_checkout()

    checkout = CheckoutPage(driver)
    checkout.completar_datos(datos["nombre"], datos["apellido"], datos["codigo_postal"])

    assert checkout.obtener_mensaje_error() == datos["mensaje_esperado"]
    assert "checkout-step-one" in checkout.url_actual()
