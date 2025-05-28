from fastapi import APIRouter, Body

from database.database import *
from models.fecha import Fecha
from schemas.fecha import Response, UpdateFechaModel


router = APIRouter()


@router.get("/", response_description="Fechas retrieved", response_model=Response)
async def get_fechas():
    fechas = await retrieve_fechas()
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Fecha data retrieved successfully",
        "data": fechas,
    }


@router.get("/{id}", response_description="fecha data retrieved", response_model=Response)
async def get_fecha_data(id: PydanticObjectId):
    fecha = await retrieve_fecha(id)
    if fecha:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": "fecha data retrieved successfully",
            "data": fecha,
        }
    return {
        "status_code": 404,
        "response_type": "error",
        "description": "fecha doesn't exist",
    }


@router.post(
    "/",
    response_description="fecha data added into the database",
    response_model=Response,
)
async def add_fecha_data(fecha: Fecha = Body(...)):
    new_fecha = await add_fecha(fecha)
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "fecha created successfully",
        "data": new_fecha,
    }

@router.put("/{id}", response_model=Response)
async def update_fecha(id: PydanticObjectId, req: UpdateFechaModel = Body(...)):
    updated_fecha = await update_fecha_data(id, req.dict())
    if updated_fecha:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": "fecha with ID: {} updated".format(id),
            "data": updated_fecha,
        }
    return {
        "status_code": 404,
        "response_type": "error",
        "description": "An error occurred. fecha with ID: {} not found".format(id),
        "data": False,
    }
