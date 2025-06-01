from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from auth.jwt_bearer import JWTBearer
from config.config import initiate_database
from routes.admin import router as AdminRouter
from routes.ticket import router as TicketRouter
from routes.fecha import router as FechaRouter

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

token_listener = JWTBearer()


@app.on_event("startup")
async def start_database():
    await initiate_database()


app.include_router(AdminRouter, tags=["Administrator"], prefix="/admin")
app.include_router(TicketRouter,tags=["Tickets"],prefix="/tickets",)
app.include_router(FechaRouter,tags=["Fechas"],prefix="/fechas",)
