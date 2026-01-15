from fastapi import APIRouter, Body, Depends

from database.database import *
from models.organizador import Organizador
from schemas.organizador import Response, UpdateOrganizadorModel
from auth.jwt_bearer import JWTBearer

token_listener = JWTBearer()

router = APIRouter()


@router.get("/", response_description="Organizadores retrieved", response_model=Response)
async def get_organizadores():
    organizadores = await retrieve_organizadores()
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Organizador data retrieved successfully",
        "data": organizadores,
    }


@router.get("/{id}", response_description="Organizador data retrieved", response_model=Response)
async def get_organizador_data(id: PydanticObjectId):
    organizador = await retrieve_organizador(id)
    if organizador:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": "organizador data retrieved successfully",
            "data": organizador,
        }
    return {
        "status_code": 404,
        "response_type": "error",
        "description": "organizador doesn't exist",
    }


@router.post(
    "/",
    response_description="organizador data added into the database",
    response_model=Response,
)
async def add_organizador_data(organizador: Organizador = Body(...), token: str = Depends(token_listener)):
    new_organizador = await add_organizador(organizador)
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "organizador created successfully",
        "data": new_organizador,
    }

@router.put("/{id}", response_model=Response)
async def update_organizador(id: PydanticObjectId, req: UpdateOrganizadorModel = Body(...), token: str = Depends(token_listener)):
    updated_organizador = await update_organizador_data(id, req.dict())
    if updated_organizador:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": "organizador with ID: {} updated".format(id),
            "data": updated_organizador,
        }
    return {
        "status_code": 404,
        "response_type": "error",
        "description": "An error occurred. organizador with ID: {} not found".format(id),
        "data": False,
    }
