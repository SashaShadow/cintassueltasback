from typing import List, Union

from beanie import PydanticObjectId

from models.admin import Admin
from models.ticket import Ticket
from models.fecha import Fecha
import uuid
from schemas.ticket import TicketCreate
from cruds.mp_crud import MpClass

admin_collection = Admin
ticket_collection = Ticket
fecha_collection = Fecha

async def add_admin(new_admin: Admin) -> Admin:
    admin = await new_admin.create()
    return admin

async def retrieve_tickets() -> List[Ticket]:
    tickets = await ticket_collection.all().to_list()
    return tickets

async def retrieve_fechas() -> List[Fecha]:
    fechas = await fecha_collection.all().to_list()
    return fechas


async def add_fecha(new_fecha: Fecha) -> Fecha:
    fecha = await new_fecha.create()
    return fecha

async def retrieve_fecha(id: PydanticObjectId) -> Ticket:
    fecha = await fecha_collection.get(id)
    if fecha:
        return fecha
    else:
        return None

async def update_fecha_data(id: PydanticObjectId, data: dict) -> Union[bool, Fecha]:
    des_body = {k: v for k, v in data.items() if v is not None}
    update_query = {"$set": {field: value for field, value in des_body.items()}}
    fecha = await fecha_collection.get(id)
    if fecha:
        await fecha.update(update_query)
        return fecha
    return False

async def add_ticket(new_ticket: TicketCreate) -> Ticket:
    fecha = await retrieve_fecha(new_ticket.id_fecha)

    external_reference = str(uuid.uuid4())

    ticket = Ticket(
        **new_ticket.dict(),
        importe_total=str(int(fecha.valor) * new_ticket.cantidad),
        estado_pago="pending",
        external_reference = external_reference,
        id_preferencia = "", 
        id_pago = ""
    )

    mp = MpClass(quantity=new_ticket.cantidad, valor_unidad=int(fecha.valor), fecha_desc=fecha.nombre_evento, external_reference=external_reference)
    preferencia = mp.generarPreferencia()

    ticket.id_preferencia = preferencia["id"]
    ticket.id_pago = ""

    ticket = await ticket.create()
    return preferencia["init_point"]


async def retrieve_ticket(id: PydanticObjectId) -> Ticket:
    ticket = await ticket_collection.get(id)
    if ticket:
        return ticket
    
async def retrieve_tickets_by_fecha(id: str) -> Ticket:
    query = {"id_fecha": id, "estado_pago": "approved"}
    print(query)
    tickets = await ticket_collection.find(query).to_list()
    print(tickets)
    if tickets:
        return tickets
    else:
        return []

async def delete_ticket(id: PydanticObjectId) -> bool:
    ticket = await ticket_collection.get(id)
    if ticket:
        await ticket.delete()
        return True


async def update_ticket_data(id: PydanticObjectId, data: dict) -> Union[bool, Ticket]:
    des_body = {k: v for k, v in data.items() if v is not None}
    update_query = {"$set": {field: value for field, value in des_body.items()}}
    ticket = await ticket_collection.get(id)
    if ticket:
        await ticket.update(update_query)
        return ticket
    return False



