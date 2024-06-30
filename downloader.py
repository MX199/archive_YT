import os
import yt_dlp

def download_and_save(channel_name, video_info, download_videos=True, download_thumbnails=True,
                      download_descriptions=True):
    try:
        category_dir = os.path.join(channel_name)
        if not os.path.exists(category_dir):
            os.makedirs(category_dir)

        if download_videos:
            output_template = os.path.join(category_dir, f"{video_info['title']}.mp4")
            ydl_opts = {
                'outtmpl': output_template,
                'format': 'bestvideo+bestaudio/best',  # Ensure highest quality download
                'socket_timeout': 5,
                'retries': 3,
                'writesubtitles': False,
                'writeautomaticsub': False,
                'writeinfojson': False,  # Do not write JSON metadata
                'writethumbnail': False,  # Do not download thumbnail with videos
                'quiet': True,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_info['webpage_url']])

            print(f"Downloaded video '{video_info['title']}' successfully.")

        if download_thumbnails:
            thumbnail_url = video_info['thumbnail']
            if thumbnail_url:
                thumbnail_output = os.path.join(category_dir, f"{video_info['title']}.png")
                thumbnail_opts = {
                    'outtmpl': thumbnail_output,
                    'quiet': True,
                }

                with yt_dlp.YoutubeDL(thumbnail_opts) as ydl_thumbnail:
                    ydl_thumbnail.download([thumbnail_url])

                print(f"Downloaded thumbnail for '{video_info['title']}' successfully.")

        if download_descriptions:
            description_output = os.path.join(category_dir, f"{video_info['title']}_description.txt")
            with open(description_output, 'w', encoding='utf-8') as desc_file:
                desc_file.write(video_info['description'])

            print(f"Saved description for '{video_info['title']}' successfully.")

    except Exception as e:
        print(f"Error downloading or saving '{video_info['title']}': {e}")

