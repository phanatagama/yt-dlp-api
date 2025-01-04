import yt_dlp

yt_url = "https://www.youtube.com/watch?v=spaDwYnjARY"
tiktok_url = "https://www.tiktok.com/@kevinyowilliam/video/7451188243732696326"
ig_url = "https://www.instagram.com/reels/DDwenx4yYU9/?hl=en"

def extract_yt(video_url):
    ydl_opts = {
            'cookiefile': 'cookies.txt',
            'quiet': True,
            'simulate': True,
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
    ydl_opts ={}
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
        "extractor_args": {
            "tiktok": {
                "api_hostname":"api22-normal-v4.tiktokv.com",
                "device_id": "7137940314170508802",
                "app_version":"34.0.3",
                "manifest_app_version": "340003",
                "aid": "7137940811609768961"
            }
        },
        # "check_formats": True,
        # "skip_download": True,
        # "listformats": True,
        
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return info


# res = extract_yt(yt_url)
# res = extract_insta(ig_url)
res = extract_tiktok(tiktok_url)
# print(res)

# cook = "ttwid=1%7CR1vh5IPLInokk0i-VGDupuI_V03hKIG4KBc_SL4eWaI%7C1735976821%7Cddb4ce48712f3cfdb72c2450e5187a1ad46193ad0bda211b656eafa097e552b8; Domain=.tiktok.com; Path=/; Expires=1767080821; tt_csrf_token=5ZFB7PJC-PCGNIuC0VsE_zN1RMYEf6ZdJQks; Domain=.tiktok.com; Path=/; Secure; tt_chain_token=\"8RARp65HlMVTkXVsoI2m/A==\"; Domain=.tiktok.com; Path=/; Secure; Expires=1751528821".split("; ")
# cookJson = {}
# for i in cook:
#     if("=" in i):
#         cookJson[i.split("=")[0]] =i.split("=")[1]

import json
from datetime import datetime
with open(f"{datetime.now()}-result.json", "w") as outfile: 
    json.dump(res, outfile)