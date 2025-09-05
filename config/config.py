from typing import Optional

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic_settings import BaseSettings
import models as models

class Settings(BaseSettings):
    # database configurations
    DATABASE_URL: Optional[str] = None
    MP_TOKEN: Optional[str] = None
    MP_CLIENT_SECRET:  Optional[str] = None
    PASS_GOOGLE: Optional[str] = None
    SECRET_USER: Optional[str] = None
    SECRET_PASS: Optional[str] = None
    MP_XSIGNATURE: Optional[str] = None
    YOUTUBE_API_KEY: Optional[str] = None
    CHANNEL_ID: Optional[str] = None
    PASS_RESEND:Optional[str] = None

    # JWT
    secret_key: str = "secret"
    algorithm: str = "HS256"

    class Config:
        env_file = ".env"
        from_attributes = True


async def initiate_database():
    client = AsyncIOMotorClient(Settings().DATABASE_URL)
    await init_beanie(
        database=client.get_default_database(), document_models=models.__all__
    )
