import yt_dlp
from urllib.parse import urlparse
import urllib.request as request
import os
import shutil

from fastapi.responses import StreamingResponse
from io import BytesIO
from fastapi import FastAPI, HTTPException


async def get_api_version():
    return {
        'version': '0.0.1',
    }

# download cookie and save into /tmp directory
def download_cookies():
    # get cookie from env blob url 
    cookie_blob = os.environ.get("YT_COOKIE")

    # create request to open it
    fake_useragent = 'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25'
    r = request.Request(cookie_blob, headers={'User-Agent': fake_useragent})
    f = request.urlopen(r)

    # path for store cookie is /tmp
    path = "/tmp"

    # Join various path components
    tmp_cookies = os.path.join(path, "cookies.txt")
    
    # write cookie into /tmp
    with open(tmp_cookies, "wb+") as file:
        file.write(f.read())
        file.close()
    f.close()
    return tmp_cookies

# yt-dlp will rewrite cookie, so we need to locate the cookie into /tmp which has access to write
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
    # download cookie before use it
    tmp_cookies = download_cookies()

    ydl_opts = {
        'cookiefile': tmp_cookies,
        # 'po_token':f"web+{po_token}",
        'quiet': True,
        'simulate': True,
        'skip_download': True
    }

    response = {'error': None}

    # make sure the url is valid youtube source
    parsed_url_result = urlparse(src)
    if parsed_url_result.netloc != 'www.youtube.com':
        response['error'] = 'Unsupported %s!' % src

        return response

    # extract video information
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(src, download=False)
            
            # filter response only for neccessary data
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

    # make sure it valid instagram url
    parsed_url_result = urlparse(url)
    if parsed_url_result.netloc != 'www.instagram.com':
        return json({"Error": f"Unsupported url {url}"})

    ydl_opts ={
        "skip_download": True,
        "format": "best",
    }

    # extract information
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return info
    

async def get_tiktok_video(src: str=''):
    url = src

    # make sure it valid tiktok url
    parsed_url_result = urlparse(url)
    if parsed_url_result.netloc != 'www.tiktok.com':
        return json({"Error": f"Unsupported url {url}"})

    # pass the args to yt-dlp, required app_info which is unique iid for each device
    # you can change the api_hostname if needed
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


async def get_yt_blob(src:str):
    # download cookie for yt
    tmp_cookies = download_cookies()
    # tmp_cookies = move_cookie_to_tmp()

    ydl_opts = {
        'cookiefile': tmp_cookies,
        'format': 'best',
        'quiet': True,
        "skip_download": True,
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

    # extract the url and return as stream response
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(src, download=False)
        video_url = info_dict['url']
        def generateStream(url):
            with ydl.urlopen(url) as stream:
                while True:
                    data = stream.read(4 * 1024 * 1024)  # 每次读取4MB数据，可调整大小
                    print(f"读取了 {len(data)} 字节数据")
                    if not data:
                        print("数据流读取完毕。")
                        break
                    yield data
        return StreamingResponse(generateStream(video_url), media_type="video/mp4")

    #     if not video_url:
    #         raise HTTPException(status_code=404, detail="Video URL not found")

        # response = requests.get(video_url, stream=True)
        # if response.status_code != 200:
        #     return {
        #         "message": "response.text"
        #     }
        #     raise HTTPException(status_code=500, detail="Failed to fetch video")

        # return StreamingResponse(BytesIO(response.content), media_type="video/mp4")
    # def iterfile():  # (1)
    #     with open('test_vid.mp4', mode="rb") as file_like:  # (2)
    #         yield from file_like  # (3)
    # return StreamingResponse(iterfile(), media_type="video/mp4")