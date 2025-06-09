from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from local_config import *
from fastapi.openapi.docs import get_swagger_ui_html
import secrets

from auth.jwt_bearer import JWTBearer
from config.config import initiate_database
from routes.admin import router as AdminRouter
from routes.ticket import router as TicketRouter
from routes.fecha import router as FechaRouter
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

app = FastAPI(
    docs_url=None,
    redoc_url=None,
    openapi_url="/openapi.json"  # Swagger lo necesita aunque luego lo protejas
)

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

origins = [
    "https://cintasueltas.vercel.app",
    "https://www.cintassueltas.com.ar",
    "http://localhost:3000",
]

security = HTTPBasic()
    
def verify_docs_user(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, SECRET_USER)
    correct_password = secrets.compare_digest(credentials.password, SECRET_PASS)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    
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

@app.get("/docs", include_in_schema=False)
def custom_swagger_ui(credentials: HTTPBasicCredentials = Depends(verify_docs_user)):
    return get_swagger_ui_html(openapi_url="/openapi.json", title="Documentación Segura")

@app.get("/openapi.json", include_in_schema=False)
def get_openapi(credentials: HTTPBasicCredentials = Depends(verify_docs_user)):
    return app.openapi()
