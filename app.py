from fastapi import FastAPI, Depends

from auth.jwt_bearer import JWTBearer
from config.config import initiate_database
from routes.admin import router as AdminRouter
from routes.ticket import router as TicketRouter
from routes.fecha import router as FechaRouter

app = FastAPI()

token_listener = JWTBearer()


@app.on_event("startup")
async def start_database():
    await initiate_database()


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app."}


app.include_router(AdminRouter, tags=["Administrator"], prefix="/admin")
app.include_router(TicketRouter,tags=["Tickets"],prefix="/tickets",)
app.include_router(FechaRouter,tags=["Fechas"],prefix="/fechas",dependencies=[Depends(token_listener)],)
