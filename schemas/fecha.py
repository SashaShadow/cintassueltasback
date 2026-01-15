from pydantic import BaseModel
from typing import Optional, Any
from local_config import *

collect_name = "fecha_test" if AMBIENTE == "DESARROLLO" else "fecha"

class UpdateFechaModel(BaseModel):
    valor: Optional[str]
    nombre_evento: Optional[str]
    direccion: Optional[str]
    nombre_lugar: Optional[str]
    imagen_url: Optional[str]
    activa: Optional[bool]
    descripcion: Optional[str]
    fecha: Optional[str]
    hora: Optional[str]
    doble: Optional[bool]

    class Collection:
        name = collect_name

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

class Response(BaseModel):
    status_code: int
    response_type: str
    description: str
    data: Optional[Any]

    class Config:
        json_schema_extra = {
            "example": {
                "status_code": 200,
                "response_type": "success",
                "description": "Operation successful",
                "data": "Sample data",
            }
        }
