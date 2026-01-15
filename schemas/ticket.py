from pydantic import BaseModel, EmailStr
from typing import Optional, Any
from local_config import *

collect_name = "ticket_test" if AMBIENTE == "DESARROLLO" else "ticket"

print(collect_name)
class TicketCreate(BaseModel):
    nombre: str
    email: EmailStr
    fecha: str
    cantidad: int
    id_fecha: str
    doble: bool

    class Settings:
        name = "tickets"

class UpdateTicketModel(BaseModel):
    fullname: Optional[str]
    email: Optional[EmailStr]
    course_of_study: Optional[str]
    year: Optional[int]
    gpa: Optional[float]

    class Collection:
        name = collect_name

    class Config:
        json_schema_extra = {
            "example": {
                "fullname": "Abdulazeez Abdulazeez",
                "email": "abdul@school.com",
                "course_of_study": "Water resources and environmental engineering",
                "year": 4,
                "gpa": "5.0",
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
