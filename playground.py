import yt_dlp
import json
from datetime import datetime

yt_url = "https://www.youtube.com/watch?v=spaDwYnjARY"
tiktok_url = "https://www.tiktok.com/@kevinyowilliam/video/7451188243732696326"
ig_url = "https://www.instagram.com/reels/DDwenx4yYU9/?hl=en"

def extract_yt(video_url):
    ydl_opts = {
            'cookiefile': 'cookies.txt',
            'quiet': True,
            'simulate': True,
            "skip_download": True,
            "format": "best",
        }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=False)
        response = {'links': []}
        for format_lists in info['formats']:
            if format_lists.get('acodec') is None:
                continue
            if format_lists['acodec'] != 'none' and format_lists['vcodec'] != 'none' and format_lists['resolution'] != 'audio only' and format_lists['ext'] == 'mp4':
                response['links'].append({
                    'format': format_lists['ext'],
                    'itag': format_lists['resolution'] + '(' + str(format_lists['aspect_ratio']) + ')',
                    'url': format_lists['url'],
                })
        return response

def extract_insta(url):
    ydl_opts ={
        "skip_download": True,
        "format": "best",
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return info

# Tiktok api_hostname to get original link
# api22-normal-v4.tiktokv.com ✅
# api16-normal-v4.tiktokv.com
# api16-normal-useast1a.tiktokv.com
# api16-normal-useast2a.tiktokv.com ✅
# api31-normal-useast1a.tiktokv.com
# api31-normal-useast2a.tiktokv.com
# api22-normal-c-useast1a.tiktokv.com
# api22-normal-c-useast2a.tiktokv.com
# api22-normal-c.tiktokv.com
# api16-normal-c.tiktokv.com
def extract_tiktok(url):
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


def write_file(data):
    with open(f"{datetime.now()}-result.json", "w") as outfile: 
        json.dump(data, outfile)

res = extract_yt(yt_url)
# res = extract_insta(ig_url)
# res = extract_tiktok(tiktok_url)
write_file(res)
# print(res)