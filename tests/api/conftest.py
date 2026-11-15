import pytest

from utils.api_client import ApiClient


@pytest.fixture
def api():
    """Cliente de API nuevo por test, para que las pruebas sean independientes."""
    cliente = ApiClient()
    yield cliente
    cliente.cerrar()
