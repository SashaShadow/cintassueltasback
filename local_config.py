import os
from dotenv import load_dotenv
load_dotenv()

mongo_db_uri = os.getenv("DATABASE_URL")

MP_TOKEN = os.getenv("MP_TOKEN")
MP_XSIGNATURE = os.getenv("MP_XSIGNATURE")
MP_CLIENT_SECRET = os.getenv("MP_CLIENT_SECRET")
PASS_GOOGLE=os.getenv("PASS_GOOGLE")
SECRET_USER=os.getenv("SECRET_USER")
SECRET_PASS=os.getenv("SECRET_PASS")
CHANNEL_ID=os.getenv("CHANNEL_ID")
YOUTUBE_API_KEY=os.getenv("YOUTUBE_API_KEY")
PASS_RESEND=os.getenv("PASS_RESEND")
AMBIENTE=os.getenv("AMBIENTE")