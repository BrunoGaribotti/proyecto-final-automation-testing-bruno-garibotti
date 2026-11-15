"""Pruebas de API sobre JSONPlaceholder (https://jsonplaceholder.typicode.com).

Cubre GET, POST, PUT, PATCH y DELETE, escenarios de éxito y de error,
validación de estructura JSON y un flujo encadenado.
"""

import pytest

from utils.data_loader import leer_json

NUEVOS_POSTS = leer_json("api_posts.json")["nuevos_posts"]
CAMPOS_POST = {"userId": int, "id": int, "title": str, "body": str}


def validar_estructura_post(post):
    """Comprueba que el post tenga todos los campos esperados con el tipo correcto."""
    for campo, tipo in CAMPOS_POST.items():
        assert campo in post, f"Falta el campo '{campo}' en {post}"
        assert isinstance(post[campo], tipo), f"'{campo}' debería ser {tipo.__name__}"


@pytest.mark.api
def test_get_listado_de_posts(api):
    respuesta = api.get("/posts")

    assert respuesta.status_code == 200
    assert "application/json" in respuesta.headers["Content-Type"]
    assert respuesta.elapsed.total_seconds() < 5

    posts = respuesta.json()
    assert isinstance(posts, list)
    assert len(posts) == 100
    for post in posts:
        validar_estructura_post(post)


@pytest.mark.api
def test_get_post_por_id(api):
    respuesta = api.get("/posts/1")

    assert respuesta.status_code == 200
    post = respuesta.json()
    validar_estructura_post(post)
    assert post["id"] == 1
    assert post["userId"] == 1


@pytest.mark.api
def test_get_posts_filtrados_por_usuario(api):
    respuesta = api.get("/posts", params={"userId": 3})

    assert respuesta.status_code == 200
    posts = respuesta.json()
    assert len(posts) > 0
    assert all(post["userId"] == 3 for post in posts)


@pytest.mark.api
def test_get_post_inexistente_devuelve_404(api):
    """Escenario de error: un recurso que no existe."""
    respuesta = api.get("/posts/99999")

    assert respuesta.status_code == 404
    assert respuesta.json() == {}


@pytest.mark.api
@pytest.mark.parametrize("nuevo_post", NUEVOS_POSTS, ids=[p["title"] for p in NUEVOS_POSTS])
def test_post_crear_post(api, nuevo_post):
    respuesta = api.post("/posts", nuevo_post)

    assert respuesta.status_code == 201
    creado = respuesta.json()
    validar_estructura_post(creado)
    assert creado["title"] == nuevo_post["title"]
    assert creado["body"] == nuevo_post["body"]
    assert creado["userId"] == nuevo_post["userId"]


@pytest.mark.api
def test_put_reemplazar_post(api):
    datos = {"id": 1, "title": "Título reemplazado", "body": "Cuerpo nuevo", "userId": 1}
    respuesta = api.put("/posts/1", datos)

    assert respuesta.status_code == 200
    assert respuesta.json() == datos


@pytest.mark.api
def test_patch_actualizar_titulo(api):
    respuesta = api.patch("/posts/1", {"title": "Sólo cambia el título"})

    assert respuesta.status_code == 200
    post = respuesta.json()
    assert post["title"] == "Sólo cambia el título"
    # PATCH es una actualización parcial: el resto de los campos se mantiene.
    assert post["id"] == 1 and post["body"] != ""


@pytest.mark.api
def test_delete_post(api):
    respuesta = api.delete("/posts/1")

    # JSONPlaceholder simula el borrado devolviendo 200 y un cuerpo vacío.
    assert respuesta.status_code == 200
    assert respuesta.json() == {}


@pytest.mark.api
@pytest.mark.e2e
def test_flujo_encadenado_usuario_y_sus_posts(api):
    """Encadenamiento: se obtiene un post, y con su userId se consulta el usuario
    autor y luego los comentarios de ese mismo post."""
    post = api.get("/posts/5").json()

    usuario = api.get(f"/users/{post['userId']}")
    assert usuario.status_code == 200
    assert usuario.json()["id"] == post["userId"]
    assert "@" in usuario.json()["email"]

    comentarios = api.get(f"/posts/{post['id']}/comments")
    assert comentarios.status_code == 200
    assert len(comentarios.json()) > 0
    assert all(c["postId"] == post["id"] for c in comentarios.json())


@pytest.mark.api
@pytest.mark.e2e
def test_flujo_crear_y_luego_actualizar_y_borrar(api):
    """Encadenamiento: el id devuelto por el POST se usa en el PATCH y el DELETE.

    JSONPlaceholder no guarda los recursos creados (siempre devuelve id 101), así
    que se actualiza/borra un post existente con el userId obtenido del POST.
    """
    creado = api.post("/posts", NUEVOS_POSTS[0])
    assert creado.status_code == 201
    id_creado = creado.json()["id"]
    assert id_creado == 101

    actualizado = api.patch("/posts/1", {"userId": creado.json()["userId"]})
    assert actualizado.status_code == 200
    assert actualizado.json()["userId"] == NUEVOS_POSTS[0]["userId"]

    borrado = api.delete("/posts/1")
    assert borrado.status_code == 200
