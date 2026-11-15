"""Page Object del carrito de compras."""

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CartPage(BasePage):
    RUTA = "cart.html"

    LISTA = (By.CLASS_NAME, "cart_list")
    ITEMS = (By.CLASS_NAME, "cart_item")
    NOMBRE_ITEM = (By.CLASS_NAME, "inventory_item_name")
    BOTON_CHECKOUT = (By.ID, "checkout")

    def obtener_nombres_items(self):
        self.esperar_url(self.RUTA)
        # Esperar a que el carrito termine de renderizarse antes de leer los ítems.
        self.encontrar(self.LISTA)
        self.encontrar(self.BOTON_CHECKOUT)
        return [i.find_element(*self.NOMBRE_ITEM).text for i in self.encontrar_todos(self.ITEMS)]

    def ir_al_checkout(self):
        self.click(self.BOTON_CHECKOUT)
