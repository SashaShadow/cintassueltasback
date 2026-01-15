from typing import Optional, Any

from beanie import Document
from pydantic import BaseModel
from local_config import *

collect_name = "fecha_test" if AMBIENTE == "DESARROLLO" else "fecha"

class Fecha(Document):
    valor: str
    nombre_evento: str
    direccion: str
    nombre_lugar: str
    imagen_url: str
    activa: bool
    descripcion: str
    fecha: str
    hora: str
    doble: bool

    class Config:
        json_schema_extra = {
            "example": {
                "valor": "4000",
                "nombre_evento": "Cintas Sueltas Fest 6",
                "direccion": "Cordoba 2860",
                "nombre_lugar": "Casa de Sasha",
                "imagen_url": "",
                "activa": True,
                "descripcion": "festival numero 6 de CS",
                "fecha": "7/6/2025",
                "hora": "20:00",
                "doble": False
            }
        }

    class Settings:
        name = collect_name
