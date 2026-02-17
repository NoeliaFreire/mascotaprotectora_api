from app.models import Mascota, MascotaCreate

class PetService:
    def __init__(self):
        self.mascotas = []
        self.counter = 1

    def create_pet(self, mascota: MascotaCreate) -> Mascota:
        nueva_mascota = Mascota(id=self.counter, **mascota.model_dump())
        self.mascotas.append(nueva_mascota)
        self.counter += 1
        return nueva_mascota

    def available_young(self, max_age: int) -> list[Mascota]:
        """
        Lógica de negocio:
        Recuperar mascotas NO adoptadas Y menores de una edad (max_age).
        """
        resultado = []
        for mascota in self.mascotas:
            # Filtro booleano (no adoptada) + Numérico (menor que max_age)
            if not mascota.adoptada and mascota.edad < max_age:
                resultado.append(mascota)
        return resultado

# Instancia global para simular persistencia en memoria
pet_service = PetService()