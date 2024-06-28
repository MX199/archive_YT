import os
import json
import yt_dlp

def create_channel_dirs(channel_name):
    channel_dir = os.path.join(channel_name)

    os.makedirs(channel_dir, exist_ok=True)




def extract_video_info(channel_url, cache_file=None):
    if cache_file and os.path.isfile(cache_file):
        with open(cache_file, "r", encoding="utf-8") as f:
            return json.load(f)

    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'writesubtitles': False,
        'writeautomaticsub': False,
        'writeinfojson': True,
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(channel_url, download=False)

    cleaned_result = []
    if 'entries' in result:
        for entry in result['entries']:
            if isinstance(entry, dict):
                video_info = {
                    'id': entry.get('id', ''),
                    'title': entry.get('title', ''),
                    'description': entry.get('description', ''),
                    'thumbnail': entry.get('thumbnails', [{}])[0].get('url', '') if 'thumbnails' in entry else '',
                    'webpage_url': entry.get('webpage_url', ''),
                }
                cleaned_result.append(video_info)

    cleaned_result = cleaned_result[:50]

    if cache_file:
        with open(cache_file, "w", encoding="utf-8") as f:
            json.dump(cleaned_result, f, ensure_ascii=False, indent=4)

    return cleaned_result
