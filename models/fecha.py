from typing import Optional, Any

from beanie import Document
from pydantic import BaseModel


class Fecha(Document):
    valor: str
    nombre_evento: str
    direccion: str
    nombre_lugar: str
    imagen_url: str
    activa: bool
    descripcion: str

    class Config:
        json_schema_extra = {
            "example": {
                "valor": "4000",
                "nombre_evento": "Cintas Sueltas Fest 6",
                "direccion": "Cordoba 2860",
                "nombre_lugar": "Casa de Sasha",
                "imagen_url": "",
                "activa": True,
                "descripcion": "festival numero 6 de CS"
            }
        }

    class Settings:
        name = "fecha"
