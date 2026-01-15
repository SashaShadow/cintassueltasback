from pydantic import BaseModel
from typing import Optional, Any
from local_config import *

collect_name = "organizadores_test" if AMBIENTE == "DESARROLLO" else "organizadores"

class UpdateOrganizadorModel(BaseModel):
    nombre: Optional[str]
    client_secret: Optional[str]
    mp_token: Optional[str]
    imagen_url: Optional[str]

    class Collection:
        name = collect_name

    class Config:
        json_schema_extra = {
            "example": {
                "nombre": "4000",
                "client_secret": "Cintas Sueltas Fest 6",
                "mp_token": "Cordoba 2860",
                "imagen_url": "Casa de Sasha",
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
