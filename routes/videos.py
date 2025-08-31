from fastapi import APIRouter, Body, Depends
from local_config import *
from database.database import *
from auth.jwt_bearer import JWTBearer
import requests
import json

token_listener = JWTBearer()

router = APIRouter()


@router.get("/", response_description="Videos de YouTube retrieved")
async def get_videos():
    url_videos = f"https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={CHANNEL_ID}&type=video&maxResults=50&key={YOUTUBE_API_KEY}"

    videos = requests.get(url_videos)
    
    videos_data = json.loads(videos.content)
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Videos data retrieved successfully",
        "data": videos_data,
    }

