"""Page Object de la página de inventario (catálogo de productos)."""

import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from pages.base_page import BasePage

logger = logging.getLogger(__name__)


class InventoryPage(BasePage):
    RUTA = "inventory.html"

    LOGO = (By.CLASS_NAME, "app_logo")
    TITULO = (By.CSS_SELECTOR, "[data-test='title']")
    PRODUCTOS = (By.CLASS_NAME, "inventory_item")
    NOMBRE_PRODUCTO = (By.CLASS_NAME, "inventory_item_name")
    PRECIO_PRODUCTO = (By.CLASS_NAME, "inventory_item_price")
    BOTON_PRODUCTO = (By.TAG_NAME, "button")
    FILTRO = (By.CLASS_NAME, "product_sort_container")
    BOTON_MENU = (By.ID, "react-burger-menu-btn")
    LINK_LOGOUT = (By.ID, "logout_sidebar_link")
    BADGE_CARRITO = (By.CLASS_NAME, "shopping_cart_badge")
    LINK_CARRITO = (By.CLASS_NAME, "shopping_cart_link")

    def esta_cargada(self):
        self.esperar_url(self.RUTA)
        return self.obtener_texto(self.TITULO) == "Products"

    def obtener_logo(self):
        return self.obtener_texto(self.LOGO)

    def obtener_titulo(self):
        return self.obtener_texto(self.TITULO)

    def obtener_productos(self):
        self.encontrar(self.PRODUCTOS)
        return self.encontrar_todos(self.PRODUCTOS)

    def obtener_nombres(self):
        return [p.find_element(*self.NOMBRE_PRODUCTO).text for p in self.obtener_productos()]

    def obtener_precios(self):
        """Devuelve los precios como float (sin el signo $)."""
        return [
            float(p.find_element(*self.PRECIO_PRODUCTO).text.replace("$", ""))
            for p in self.obtener_productos()
        ]

    def obtener_datos_producto(self, indice=0):
        producto = self.obtener_productos()[indice]
        return {
            "nombre": producto.find_element(*self.NOMBRE_PRODUCTO).text,
            "precio": producto.find_element(*self.PRECIO_PRODUCTO).text,
        }

    def agregar_producto_por_nombre(self, nombre):
        logger.info("Agregando al carrito: %s", nombre)
        for producto in self.obtener_productos():
            if producto.find_element(*self.NOMBRE_PRODUCTO).text == nombre:
                producto.find_element(*self.BOTON_PRODUCTO).click()
                return
        raise ValueError(f"No se encontró el producto '{nombre}' en el inventario")

    def agregar_producto_por_indice(self, indice=0):
        producto = self.obtener_productos()[indice]
        nombre = producto.find_element(*self.NOMBRE_PRODUCTO).text
        logger.info("Agregando al carrito: %s", nombre)
        producto.find_element(*self.BOTON_PRODUCTO).click()
        return nombre

    def ordenar_por(self, texto_opcion):
        logger.info("Ordenando productos por: %s", texto_opcion)
        Select(self.encontrar(self.FILTRO)).select_by_visible_text(texto_opcion)

    def cantidad_en_carrito(self):
        if not self.esta_visible(self.BADGE_CARRITO):
            return 0
        return int(self.obtener_texto(self.BADGE_CARRITO))

    def ir_al_carrito(self):
        self.click(self.LINK_CARRITO)

    def filtro_visible(self):
        return self.esta_visible(self.FILTRO)

    def menu_visible(self):
        return self.esta_visible(self.BOTON_MENU)

    def logout(self):
        logger.info("Cerrando sesión")
        self.click(self.BOTON_MENU)
        self.click(self.LINK_LOGOUT)
