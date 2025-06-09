from fastapi import Body, APIRouter, HTTPException, Depends, status, Request
from passlib.context import CryptContext
from auth.jwt_handler import sign_jwt
from database.database import add_admin
from models.admin import Admin
from schemas.admin import AdminData, AdminSignIn
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
from local_config import *
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

hash_helper = CryptContext(schemes=["bcrypt"])

security = HTTPBasic()

def verify_admin(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, SECRET_USER)
    correct_password = secrets.compare_digest(credentials.password, SECRET_PASS)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    
router = APIRouter()

@router.post("/login")
@limiter.limit("5/minute")
async def admin_login(request: Request, admin_credentials: AdminSignIn = Body(...)):
    admin_exists = await Admin.find_one(Admin.email == admin_credentials.username)
    if admin_exists:
        password = hash_helper.verify(admin_credentials.password, admin_exists.password)
        if password:
            return sign_jwt(admin_credentials.username)

        raise HTTPException(status_code=403, detail="Contraseña o email incorrectos")

    raise HTTPException(status_code=403, detail="Contraseña o email incorrectos")


@router.post("", response_model=AdminData)
@limiter.limit("5/minute")
async def admin_signup(request: Request, admin: Admin = Body(...), credentials: HTTPBasicCredentials = Depends(verify_admin)):
    admin_exists = await Admin.find_one(Admin.email == admin.email)
    if admin_exists:
        raise HTTPException(
            status_code=409, detail="Admin with email supplied already exists"
        )

    admin.password = hash_helper.encrypt(admin.password)
    new_admin = await add_admin(admin)
    return new_admin
