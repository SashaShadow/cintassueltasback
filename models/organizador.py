from beanie import Document
from local_config import *

collect_name = "organizadores_test" if AMBIENTE == "DESARROLLO" else "organizadores"

class Organizador(Document):
    nombre: str
    client_secret: str
    mp_token: str
    imagen_url: str

    class Config:
        json_schema_extra = {
            "example": {
                "nombre": "Cintas Sueltas",
                "client_secret": "asdawr23523523",
                "mp_token": "aserje1234",
                "imagen_url": "www.xd.com/img.jpg",
            }
        }

    class Settings:
        name = collect_name
