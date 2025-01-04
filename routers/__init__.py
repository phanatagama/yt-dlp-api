from .video import *
from fastapi import APIRouter


info_router = APIRouter(tags=['API version'])
info_router.add_api_route('/', get_api_version, methods=['GET'])

ping_router = APIRouter(tags=['API ping'])
ping_router.add_api_route('/ping', ping, methods=['GET'])

video_info_router = APIRouter(tags=['Extract video_info'])
video_info_router.add_api_route('/video/', extract_video_info, methods=['GET'])
