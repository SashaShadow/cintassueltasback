from fastapi import APIRouter, Body, Depends
from local_config import *
from database.database import *
from auth.jwt_bearer import JWTBearer
import requests
import json

token_listener = JWTBearer()

router = APIRouter()


@router.get("/{limit}", response_description="Videos de YouTube retrieved")
async def get_videos(limit):
    url_videos = f"https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={CHANNEL_ID}&type=video&maxResults={limit}&order=date&key={YOUTUBE_API_KEY}"

    videos = requests.get(url_videos)
    
    videos_data = json.loads(videos.content)
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Videos data retrieved successfully",
        "data": videos_data,
    }

@router.get("/playlists/{limit}", response_description="Playlists del canal")
async def get_playlists(limit: int = 10):

    url = f"https://www.googleapis.com/youtube/v3/playlists?part=snippet&channelId={CHANNEL_ID}&maxResults={limit}&key={YOUTUBE_API_KEY}"
    response = requests.get(url)
    data = response.json()
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Playlists del canal obtenidas exitosamente",
        "data": data,
    }

@router.get("/playlist/{playlist_id}/{limit}", response_description="Videos de una playlist")
async def get_videos_from_playlist(playlist_id: str, limit: int = 10):
    url = f"https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId={playlist_id}&maxResults={limit}&order=date&key={YOUTUBE_API_KEY}"
    response = requests.get(url)
    data = response.json()
    return {
        "status_code": 200,
        "response_type": "success",
        "description": f"Videos de la playlist {playlist_id} obtenidos exitosamente",
        "data": data,
    }
