from pydantic import BaseModel
from typing import Optional

class MascotaBase(BaseModel):
    nombre: str
    especie: str
    edad: int
    adoptada: bool = False  # Por defecto no está adoptada

class MascotaCreate(MascotaBase):
    pass

class Mascota(MascotaBase):
    id: int

    class Config:
        from_attributes = True