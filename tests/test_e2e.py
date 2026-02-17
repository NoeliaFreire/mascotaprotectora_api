import pytest
import httpx

# URL base donde estará corriendo la API (definida en el pipeline)
BASE_URL = "http://localhost:8000"

@pytest.mark.e2e
def test_create_and_filter_pets_e2e():
    """
    Test completo: Crea mascota -> Verifica creación -> Filtra.
    """
    # 1. Crear una mascota
    payload = {
        "nombre": "Firulais",
        "especie": "Perro",
        "edad": 3,
        "adoptada": False
    }
    response_post = httpx.post(f"{BASE_URL}/mascotas", json=payload)
    assert response_post.status_code == 201
    data = response_post.json()
    assert data["nombre"] == "Firulais"
    assert "id" in data

    # 2. Consultar el endpoint de filtro
    # Buscamos menores de 5 años (Firulais tiene 3, debería salir)
    response_get = httpx.get(f"{BASE_URL}/mascotas/disponibles", params={"max_age": 5})
    assert response_get.status_code == 200
    mascotas = response_get.json()
    
    # Verificamos que al menos una es la que acabamos de crear
    nombres = [m["nombre"] for m in mascotas]
    assert "Firulais" in nombres