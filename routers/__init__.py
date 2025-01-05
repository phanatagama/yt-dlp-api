from .video import *
from fastapi import APIRouter


info_router = APIRouter(tags=['API version'])
info_router.add_api_route('/', get_api_version, methods=['GET'])

tiktok_router = APIRouter(tags=['API tiktok'])
tiktok_router.add_api_route('/tiktok', get_tiktok_video, methods=['GET'])

instagram_router = APIRouter(tags=['API Instagram reel'])
instagram_router.add_api_route('/instagram', get_reel_video, methods=['GET'])

video_info_router = APIRouter(tags=['Extract youtube'])
video_info_router.add_api_route('/youtube', extract_video_info, methods=['GET'])

yt_blob_router = APIRouter(tags=['get blob youtube'])
yt_blob_router.add_api_route('/blob', get_yt_blob, methods=['GET'])
