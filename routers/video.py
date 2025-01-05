import yt_dlp
from urllib.parse import urlparse
import os
import shutil

from fastapi.responses import StreamingResponse
from io import BytesIO
from fastapi import FastAPI, HTTPException


async def get_api_version():
    return {
        'version': '0.0.1',
    }

def move_cookie_to_tmp():
    # cookies_file = "cookies.txt"  # Path to your cookies file
    # copy cookies.txt into /tmp
    path = "/tmp"

    # Join various path components
    tmp_cookies = os.path.join(path, "cookies.txt")

    dest = shutil.copyfile("cookies.txt", tmp_cookies)
    return tmp_cookies
    
async def extract_video_info(src: str = ''):
    # po_token ="MnQ4RCUX1rkNwTh8YuYQC-fXgf_g3KsJY3NyPsBPBUBzQRBT6q0ZHOE7QPT4k8WRvAXqpRUps_NkCGVvZN6OuwYL0ItXqkMi4iqfWjvDrKduMM2kckSI7nwU1W2ElNr_1aqIQ1M3gLWQqxM9IunkAos9X4dCSA=="
    tmp_cookies = move_cookie_to_tmp()

    ydl_opts = {
        'cookiefile': tmp_cookies,
        # 'po_token':f"web+{po_token}",
        'quiet': True,
        'simulate': True,
        'skip_download': True
    }

    response = {'error': None}

    parsed_url_result = urlparse(src)
    if parsed_url_result.netloc != 'www.youtube.com':
        response['error'] = 'Unsupported %s!' % src

        return response

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(src, download=False)
            response = info.copy()
            response["formats"] = []
            del response["thumbnails"]
            del response["automatic_captions"]
            del response["heatmap"]
            del response["chapters"]

            # response = {'links': []}
            for format_lists in info['formats']:
                if format_lists.get('acodec') is None:
                    continue
                if format_lists['acodec'] != 'none' and format_lists['vcodec'] != 'none' and format_lists['resolution'] != 'audio only' and format_lists['ext'] == 'mp4':
                    response["formats"].append(format_lists)
                    
            # response = {'links': info["url"]}
            # for format_lists in info['formats']:
            #     if format_lists.get('acodec') is None:
            #         continue
            #     if format_lists['acodec'] != 'none' and format_lists['vcodec'] != 'none' and format_lists['resolution'] != 'audio only' and format_lists['ext'] == 'mp4':
            #         response['links'].append({
            #             'format': format_lists['ext'],
            #             'itag': format_lists['resolution'] + '(' + str(format_lists['aspect_ratio']) + ')',
            #             'url': format_lists['url'],
            #         })

        except Exception as e:
            response['error'] = str(e)


    return response

async def get_reel_video(src: str =''):
    url = src
    parsed_url_result = urlparse(url)
    if parsed_url_result.netloc != 'www.instagram.com':
        return json({"Error": f"Unsupported url {url}"})

    ydl_opts ={
        "skip_download": True,
        "format": "best",
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return info
    

async def get_tiktok_video(src: str=''):
    url = src

    parsed_url_result = urlparse(url)
    if parsed_url_result.netloc != 'www.tiktok.com':
        return json({"Error": f"Unsupported url {url}"})

    ydl_opts ={
        "skip_download": True,
        "format": "best",
        "extractor_args": {
            "tiktok": {
                # "api_hostname": ["api16-normal-c-useast1a.tiktokv.com"],
                "app_info": ["7318518857994389254"],
                "device_id": ["7318517321748022790"],
                "app_version":["34.0.3"],
                "manifest_app_version": ["340003"],
                "aid": ["7137940811609768961"]
            }
        },
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return info


async def get_yt_blob(src: str):
    tmp_cookies = move_cookie_to_tmp()

    ydl_opts = {
        'cookiefile': tmp_cookies,
        'format': 'best',
        'quiet': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(src, download=False)
        video_url = info_dict['url']

        if not video_url:
            raise HTTPException(status_code=404, detail="Video URL not found")

        response = requests.get(video_url, stream=True)
        if response.status_code != 200:
            return {
                "message": "response.text"
            }
        #     raise HTTPException(status_code=500, detail="Failed to fetch video")

        return {
            "url": video_url
        }
        # return StreamingResponse(BytesIO(response.content), media_type="video/mp4")