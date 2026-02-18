from app.service import PetService
from app.models import MascotaCreate
def test_available_young_logic():
    # Setup: Creamos un servicio aislado
    service = PetService()
    
    # Añadimos datos de prueba
    # 1. Joven y no adoptada (Debería salir)
    service.create_pet(MascotaCreate(nombre="Rex", especie="Perro", edad=2, adoptada=False))
    # 2. Vieja y no adoptada (No debería salir por edad)
    service.create_pet(MascotaCreate(nombre="Laika", especie="Perro", edad=10, adoptada=False))
    # 3. Joven pero adoptada (No debería salir por estado)
    service.create_pet(MascotaCreate(nombre="Michi", especie="Gato", edad=1, adoptada=True))

    # Ejecución: Buscamos menores de 5 años
    resultados = service.available_young(max_age=5)

    # Aserciones
    assert len(resultados) == 1
    assert resultados[0].nombre == "Rex"
    assert resultados[0].edad == 2