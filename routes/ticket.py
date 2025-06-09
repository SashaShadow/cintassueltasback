from fastapi import APIRouter, Depends, Request

from database.database import *
from schemas.ticket import Response, TicketCreate
from pydantic import BaseModel
from pymongo import MongoClient
from database.database_mongo import get_mongo_db 
from cruds.mp_crud import MpClass
from fastapi.responses import JSONResponse # type: ignore
import urllib.parse
from typing import Union

router = APIRouter()


@router.get("/", response_description="Tickets retrieved", response_model=Response)
async def get_tickets():
    tickets = await retrieve_tickets()
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Ticket data retrieved successfully",
        "data": tickets,
    }


@router.get("/{id}", response_description="ticket data retrieved", response_model=Response)
async def get_ticket_data(id: PydanticObjectId):
    ticket = await retrieve_ticket(id)
    if ticket:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": "ticket data retrieved successfully",
            "data": ticket,
        }
    return {
        "status_code": 404,
        "response_type": "error",
        "description": "ticket doesn't exist",
        "data": None
    }

@router.get("/byfecha/{id}", response_description="ticket data retrieved", response_model=Response)
async def get_ticket_data_by_fecha(id: str):
    tickets = await retrieve_tickets_by_fecha(id)
    if tickets:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": "tickets data retrieved successfully",
            "data": tickets,
        }
    return {
        "status_code": 404,
        "response_type": "error",
        "description": "tickets doesn't exist",
        "data": None
    }


@router.post(
    "/",
    response_description="ticket data added into the database",
    response_model=Response,
)
async def add_ticket_data(ticket: TicketCreate):
    new_ticket = await add_ticket(ticket)
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "ticket created successfully",
        "data": new_ticket,
    }

class MpPayment(BaseModel):
    id: str

class WebhookRequest(BaseModel):
    id: int
    live_mode: bool
    type: str
    date_created: str
    user_id: Union[int, str]
    api_version: str
    action: str
    data: MpPayment

@router.post("/mp-notificacion")
async def recibir_webhook(
    request_body: WebhookRequest,
    request: Request,
    db: MongoClient = Depends(get_mongo_db)
):
    try:
        payload_notificacion = request_body.data
        print(payload_notificacion)
        
        xSignature = request.headers.get("x-signature")
        xRequestId = request.headers.get("x-request-id")
        
        # Obtain Query params related to the request URL
        queryParams = urllib.parse.parse_qs(request.url.query)

        # Extract the "data.id" from the query params
        dataID = queryParams.get("data.id", [""])[0]

        print(queryParams)
        print(dataID)
        
        if xRequestId is None or xSignature is None:
            return JSONResponse(content={"Mensaje": 'Headers no presentes'}, status_code=200) 
        
        parts = xSignature.split(",")
        ts = None
        hash = None

        for part in parts:
            keyValue = part.split("=", 1)
            if len(keyValue) == 2:
                key = keyValue[0].strip()
                value = keyValue[1].strip()
                if key == "ts":
                    ts = value
                elif key == "v1":
                    hash = value

        manifest = f"id:{dataID};request-id:{xRequestId};ts:{ts};"

        if dataID:
            mp = MpClass(db=db, id_pago=dataID, manifest=manifest, hash=hash)
            verificacion_token = mp.verificarToken()

            if verificacion_token:
                resultado_notificacion = mp.notificacion()
            else:
                resultado_notificacion = JSONResponse(content={"Mensaje": 'Error al verificar el token'}, status_code=200)
            return resultado_notificacion
        else:
            return JSONResponse(content={"Mensaje": 'Pago no encontrado'}, status_code=200) 
    except Exception as e:
        return JSONResponse(
            content={"Mensaje": f"Error interno: {str(e)}"},
            status_code=500
        )
    
class ReqUpd(BaseModel):
    estado_pago: str
    id_pago: str

@router.put("/pagoext/{external_reference}", response_model=Response)
async def actualizar_pago(external_reference: str, request_body: ReqUpd, db: MongoClient = Depends(get_mongo_db)
):
    try:
        estado_pago = request_body.estado_pago
        id_pago = request_body.id_pago

        mp = MpClass(external_reference=external_reference, estado_pago=estado_pago, id_pago=id_pago, db=db, origen="web")
        updated_ticket = mp.modificarEstadoPago()

        if updated_ticket:
            return {
                "status_code": 200,
                "response_type": "success",
                "description": "ticket with external_reference: {} updated".format(external_reference),
                "data": updated_ticket,
            }
        return {
            "status_code": 404,
            "response_type": "error",
            "description": "An error occurred. ticket with external_reference: {} not found".format(external_reference),
            "data": False,
        }
    except Exception as e:
        return JSONResponse(
            content={"Mensaje": f"Error interno: {str(e)}"},
            status_code=500
        )