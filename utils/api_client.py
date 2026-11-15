"""Cliente HTTP mínimo para la API pública JSONPlaceholder.

Envuelve a `requests` para centralizar la URL base, el timeout y el logging
de cada petición/respuesta.
"""

import logging

import requests

BASE_URL_API = "https://jsonplaceholder.typicode.com"
TIMEOUT = 10

logger = logging.getLogger(__name__)


class ApiClient:
    def __init__(self, base_url=BASE_URL_API):
        self.base_url = base_url
        self.sesion = requests.Session()
        self.sesion.headers.update({"Content-Type": "application/json; charset=UTF-8"})

    def _enviar(self, metodo, endpoint, **kwargs):
        url = f"{self.base_url}{endpoint}"
        logger.info("%s %s %s", metodo, url, kwargs.get("json", ""))
        respuesta = self.sesion.request(metodo, url, timeout=TIMEOUT, **kwargs)
        logger.info(
            "Respuesta %s en %.3fs: %s",
            respuesta.status_code,
            respuesta.elapsed.total_seconds(),
            respuesta.text[:200],
        )
        return respuesta

    def get(self, endpoint, **kwargs):
        return self._enviar("GET", endpoint, **kwargs)

    def post(self, endpoint, datos):
        return self._enviar("POST", endpoint, json=datos)

    def put(self, endpoint, datos):
        return self._enviar("PUT", endpoint, json=datos)

    def patch(self, endpoint, datos):
        return self._enviar("PATCH", endpoint, json=datos)

    def delete(self, endpoint):
        return self._enviar("DELETE", endpoint)

    def cerrar(self):
        self.sesion.close()
