from typing import Optional, Any

from beanie import Document
from pydantic import BaseModel, EmailStr
from local_config import *

collect_name = "ticket_test" if AMBIENTE == "DESARROLLO" else "ticket"

class Ticket(Document):
    nombre: str
    email: EmailStr
    fecha: str
    cantidad: int
    id_fecha: str
    importe_total: str
    estado_pago: str
    external_reference: str
    id_preferencia: str
    id_pago: str

    class Config:
        json_schema_extra = {
            "example": {
                "nombre": "Abdulazeez Abdulazeez Adeshina",
                "email": "abdul@school.com",
                "fecha": "2025-05-01",
                "cantidad": 4,
                "id_fecha": "35osf359ats0as0as0t00",
            }
        }

    class Settings:
        name = collect_name
