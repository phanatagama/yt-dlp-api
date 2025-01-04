import yt_dlp
from urllib.parse import urlparse


async def get_api_version():
    return {
        'version': '0.0.1',
    }

async def extract_video_info(video_url: str = ''):
    # po_token ="MnQ4RCUX1rkNwTh8YuYQC-fXgf_g3KsJY3NyPsBPBUBzQRBT6q0ZHOE7QPT4k8WRvAXqpRUps_NkCGVvZN6OuwYL0ItXqkMi4iqfWjvDrKduMM2kckSI7nwU1W2ElNr_1aqIQ1M3gLWQqxM9IunkAos9X4dCSA=="
    cookies_file = "cookies.txt"  # Path to your cookies file

    ydl_opts = {
        'cookiefile': cookies_file,
        'po_token':f"web+{po_token}",
        'quiet': True,
        'simulate': True,
    }

    response = {'error': None}

    parsed_url_result = urlparse(video_url)
    if parsed_url_result.netloc != 'www.youtube.com':
        response['error'] = 'Unsupported %s!' % video_url

        return response

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(video_url)

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

        except Exception as e:
            response['error'] = str(e)


    return response
