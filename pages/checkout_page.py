"""Page Object de los pasos del checkout (datos, resumen y confirmación)."""

import logging

from selenium.webdriver.common.by import By

from pages.base_page import BasePage

logger = logging.getLogger(__name__)


class CheckoutPage(BasePage):
    # Paso 1: datos del comprador
    CAMPO_NOMBRE = (By.ID, "first-name")
    CAMPO_APELLIDO = (By.ID, "last-name")
    CAMPO_CODIGO_POSTAL = (By.ID, "postal-code")
    BOTON_CONTINUAR = (By.ID, "continue")
    MENSAJE_ERROR = (By.CSS_SELECTOR, "[data-test='error']")

    # Paso 2: resumen
    NOMBRE_ITEM = (By.CLASS_NAME, "inventory_item_name")
    TOTAL = (By.CLASS_NAME, "summary_total_label")
    BOTON_FINALIZAR = (By.ID, "finish")

    # Paso 3: confirmación
    MENSAJE_CONFIRMACION = (By.CLASS_NAME, "complete-header")

    def completar_datos(self, nombre, apellido, codigo_postal):
        logger.info("Completando datos de checkout: %s %s (%s)", nombre, apellido, codigo_postal)
        self.escribir(self.CAMPO_NOMBRE, nombre)
        self.escribir(self.CAMPO_APELLIDO, apellido)
        self.escribir(self.CAMPO_CODIGO_POSTAL, codigo_postal)
        self.click(self.BOTON_CONTINUAR)

    def obtener_mensaje_error(self):
        return self.obtener_texto(self.MENSAJE_ERROR)

    def obtener_items_resumen(self):
        self.encontrar(self.TOTAL)
        return [e.text for e in self.encontrar_todos(self.NOMBRE_ITEM)]

    def obtener_total(self):
        return self.obtener_texto(self.TOTAL)

    def finalizar_compra(self):
        logger.info("Finalizando la compra")
        self.click(self.BOTON_FINALIZAR)

    def obtener_mensaje_confirmacion(self):
        return self.obtener_texto(self.MENSAJE_CONFIRMACION)
