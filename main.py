import os
import json
import time
import logging
import asyncio
from utilities import create_channel_dirs, extract_video_info
from downloader import download_and_save


logo = """
\033[91m 

███████████████████████████████████████████████████
██▀▄─██▄─▄▄▀█─▄▄▄─█─█─█▄─▄█▄─█─▄█▄─▄▄─█▄─█─▄█─▄─▄─█
██─▀─███─▄─▄█─███▀█─▄─██─███▄▀▄███─▄█▀██▄─▄████─███
▀▄▄▀▄▄▀▄▄▀▄▄▀▄▄▄▄▄▀▄▀▄▀▄▄▄▀▀▀▄▀▀▀▄▄▄▄▄▀▀▄▄▄▀▀▀▄▄▄▀▀
by MX199 https://github.com/MX199/archive_YT
\033[0m
"""


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_config():
    config_path = 'config.json'
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
            logging.info("Configuration loaded successfully.")
            return config
    except FileNotFoundError:
        logging.error(f"Configuration file {config_path} not found.")
        raise
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON from {config_path}: {e}")
        raise

def fetch_videos(channel_url):
    logging.info(f"Fetching video information from {channel_url}...")
    # Simulate loading bar
    print("\033[91mFetching videos:\033[0m ", end="", flush=True)
    for _ in range(10):
        time.sleep(0.1)
        print("\033[91m█\033[0m", end="", flush=True)
    print("")
    return extract_video_info(channel_url)

async def download_content_async(channel_name, video_info, download_videos, download_thumbnails, download_descriptions):
    await asyncio.to_thread(download_and_save, channel_name, video_info, download_videos, download_thumbnails, download_descriptions)
    return {
        'title': video_info['title'],
        'description': video_info.get('description'),
        'thumbnail': video_info.get('thumbnail'),
        'webpage_url': video_info['webpage_url'],
    }

def sanitize_filename(name):
    return "".join(c for c in name if c.isalnum() or c in (' ', '.', '_')).rstrip()

async def process_videos(channel_name, type_yt, download_videos, download_thumbnails, download_descriptions, output_file):
    channel_url = f"https://www.youtube.com/@{channel_name}/{type_yt}"
    create_channel_dirs(channel_name)
    channel_info = fetch_videos(channel_url)

    cleaned_video_info = []
    print(f"\033[91mProcessing videos:\033[0m ")

    tasks = [
        download_content_async(channel_name, video_info, download_videos, download_thumbnails, download_descriptions)
        for video_info in channel_info
    ]

    for task in asyncio.as_completed(tasks):
        cleaned_video_info.append(await task)

    videos_info_path = os.path.join(channel_name, sanitize_filename(output_file))
    with open(videos_info_path, 'w', encoding='utf-8') as f:
        json.dump(cleaned_video_info, f, ensure_ascii=False, indent=4)

    print("\033[91mDownload and processing completed!\033[0m")

def main(channel_name, type_yt, option):
    options_map = {
        '1': (True, True, True, f"{channel_name} - info.json"),
        '2': (False, True, False, f"{channel_name} - thumbnails_only_info.json"),
        '3': (False, False, True, f"{channel_name} - descriptions_only_info.json"),
        '4': (True, True, False, f"{channel_name} - videos_and_thumbnails_info.json"),
    }
    download_videos, download_thumbnails, download_descriptions, output_file = options_map[option]

    loop = asyncio.get_event_loop()
    loop.run_until_complete(process_videos(channel_name, type_yt, download_videos, download_thumbnails, download_descriptions, output_file))

def print_menu():
    print(logo)
    print("Select an option:")
    print("1. Download and process videos")
    print("2. Download thumbnails only")
    print("3. Download descriptions only")
    print("4. Download both videos and thumbnails")
    print("5. Exit")

def interactive_menu():
    while True:
        print_menu()
        channel_name = input("\033[91mEnter the name of the YouTube channel:\033[0m ")
        type_yt = input("\033[91mDo you want to download videos or shorts? Enter 'videos' or 'shorts':\033[0m ")
        
        choice = input("\033[91mEnter your choice (1-5):\033[0m ")
        if choice == '1':
            main(channel_name, type_yt, '1')
        elif choice == '2':
            main(channel_name, type_yt, '2')
        elif choice == '3':
            main(channel_name, type_yt, '3')
        elif choice == '4':
            main(channel_name, type_yt, '4')
        elif choice == '5':
            print("\033[91mExiting...\033[0m")
            break
        else:
            print("\033[91mInvalid choice. Please enter a number from 1 to 5.\033[0m")

        input("\nPress Enter to return to the menu...")
        os.system('cls' if os.name == 'nt' else 'clear')  # Clear screen

def print_welcome_message():
    print("\033[91m")  
    for _ in range(5):
        os.system('cls' if os.name == 'nt' else 'clear')  
        print(logo)
        time.sleep(0.2)  
    print("Welcome to YouTube Channel archive!\033[0m")

if __name__ == "__main__":
    try:
        config = load_config()
    except Exception as e:
        logging.critical(f"Failed to load configuration: {e}")
        exit(1)
    
    print_welcome_message()
    interactive_menu()
