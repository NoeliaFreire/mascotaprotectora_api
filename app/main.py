from fastapi import FastAPI 
from app.models import Mascota, MascotaCreate
from app.service import pet_service

app = FastAPI(title="API Protectora de Mascotas")

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de la Protectora"}

@app.post("/mascotas", response_model=Mascota, status_code=201)
def crear_mascota(mascota: MascotaCreate):
    return pet_service.create_pet(mascota)

@app.get("/mascotas/disponibles", response_model=list[Mascota])
def listar_mascotas_jovenes(max_age: int):
    """
    Devuelve mascotas no adoptadas y menores de 'max_age'.
    """
    return pet_service.available_young(max_age)