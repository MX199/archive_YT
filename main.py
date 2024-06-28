import os
import json
import argparse
import time
from utilities import create_channel_dirs, extract_video_info
from downloader import download_and_save  # Assuming you have a downloader module

# ASCII art logo with ANSI escape sequences for red color
logo = """
\033[91m 

███████████████████████████████████████████████████
██▀▄─██▄─▄▄▀█─▄▄▄─█─█─█▄─▄█▄─█─▄█▄─▄▄─█▄─█─▄█─▄─▄─█
██─▀─███─▄─▄█─███▀█─▄─██─███▄▀▄███─▄█▀██▄─▄████─███
▀▄▄▀▄▄▀▄▄▀▄▄▀▄▄▄▄▄▀▄▀▄▀▄▄▄▀▀▀▄▀▀▀▄▄▄▄▄▀▀▄▄▄▀▀▀▄▄▄▀▀
by MX199 https://github.com/MX199
\033[0m
"""

def main(channel_name, type_yt):
    channel_url = f"https://www.youtube.com/@{channel_name}/{type_yt}"
    videos_info_file = f"{channel_name} - info.json"  # File to store processed video info

    # Create channel directory if it doesn't exist
    create_channel_dirs(channel_name)

    # Extract video information
    channel_info = extract_video_info(channel_url)

    # List to store cleaned video info
    cleaned_video_info = []

    # Print and process each video
    print(f"Fetching video information from {channel_name}...")

    # Simulate a loading bar for fetching video information
    print("\033[91mFetching videos:\033[0m ", end="", flush=True)
    for _ in range(10):
        time.sleep(0.2)  # Simulate fetching delay
        print("\033[91m█\033[0m", end="", flush=True)
    print("")

    # Simulate processing each video
    print(f"\033[91mProcessing videos:\033[0m ")
    for video_info in channel_info:
        # Simulate processing delay
        time.sleep(0.2)

        # Simulate downloading delay
        for _ in range(10):
            time.sleep(0.1)
            print("\033[91m.\033[0m", end="", flush=True)
        print("\033[91mDONE\033[0m")

        # Download and save the video
        download_and_save(
            channel_name,
            video_info,
            download_videos=True,  # Set to False to skip downloading videos
            download_thumbnails=True,  # Set to False to skip downloading thumbnails
            download_descriptions=True  # Set to False to skip saving descriptions
        )

        # Clean video info (remove unnecessary fields)
        cleaned_video_info.append({
            'title': video_info['title'],
            'description': video_info['description'],
            'thumbnail': video_info['thumbnail'],
            'webpage_url': video_info['webpage_url'],
        })

    # Write cleaned video info to channel directory
    videos_info_path = os.path.join(channel_name, videos_info_file)
    with open(videos_info_path, 'w', encoding='utf-8') as f:
        json.dump(cleaned_video_info, f, ensure_ascii=False, indent=4)

def print_menu():
    print("Select an option:")
    print("1. Download and process videos")
    print("2. Download thumbnails only")
    print("3. Download descriptions only")
    print("4. Download both videos and thumbnails")
    print("5. Exit")

def interactive_menu(channel_name, type_yt):
    while True:
        print(logo)
        print_menu()
        choice = input("\033[91mEnter your choice (1-5):\033[0m ")

        if choice == '1':
            main(channel_name, type_yt)
        elif choice == '2':
            download_thumbnails_only(channel_name, type_yt)
        elif choice == '3':
            download_descriptions_only(channel_name, type_yt)
        elif choice == '4':
            download_videos_and_thumbnails(channel_name, type_yt)
        elif choice == '5':
            print("\033[91mExiting...\033[0m")
            break
        else:
            print("\033[91mInvalid choice. Please enter a number from 1 to 5.\033[0m")

def download_thumbnails_only(channel_name, type_yt):
    channel_url = f"https://www.youtube.com/@{channel_name}/{type_yt}"
    videos_info_file = f"{channel_name} - thumbnails_only_info.json"

    # Create channel directory if it doesn't exist
    create_channel_dirs(channel_name)

    # Extract video information
    channel_info = extract_video_info(channel_url)

    # List to store cleaned video info
    cleaned_video_info = []

    # Process each video for thumbnails only
    print(f"Downloading thumbnails from {channel_name}...")

    # Simulate downloading thumbnails
    print("\033[91mDownloading thumbnails:\033[0m ", end="", flush=True)
    for _ in range(10):
        time.sleep(0.2)  # Simulate downloading delay
        print("\033[91m█\033[0m", end="", flush=True)
    print("")

    for video_info in channel_info:
        # Download and save the thumbnail only
        download_and_save(
            channel_name,
            video_info,
            download_videos=False,
            download_thumbnails=True,
            download_descriptions=False
        )

        # Clean video info (remove unnecessary fields)
        cleaned_video_info.append({
            'title': video_info['title'],
            'thumbnail': video_info['thumbnail'],
        })

    # Write cleaned video info to channel directory
    videos_info_path = os.path.join(channel_name, videos_info_file)
    with open(videos_info_path, 'w', encoding='utf-8') as f:
        json.dump(cleaned_video_info, f, ensure_ascii=False, indent=4)

def download_descriptions_only(channel_name, type_yt):
    channel_url = f"https://www.youtube.com/@{channel_name}/{type_yt}"
    videos_info_file = f"{channel_name} - descriptions_only_info.json"

    # Create channel directory if it doesn't exist
    create_channel_dirs(channel_name)

    # Extract video information
    channel_info = extract_video_info(channel_url)

    # List to store cleaned video info
    cleaned_video_info = []

    # Process each video for descriptions only
    print(f"Downloading descriptions from {channel_name}...")

    # Simulate downloading descriptions
    print("\033[91mDownloading descriptions:\033[0m ", end="", flush=True)
    for _ in range(10):
        time.sleep(0.2)
        print("\033[91m█\033[0m", end="", flush=True)
    print("")

    for video_info in channel_info:
        # Download and save the description only
        download_and_save(
            channel_name,
            video_info,
            download_videos=True,
            download_thumbnails=True,
            download_descriptions=True
        )

        cleaned_video_info.append({
            'title': video_info['title'],
            'description': video_info['description'],
        })

    # Write cleaned video info to channel directory
    videos_info_path = os.path.join(channel_name, videos_info_file)
    with open(videos_info_path, 'w', encoding='utf-8') as f:
        json.dump(cleaned_video_info, f, ensure_ascii=False, indent=4)

def download_videos_and_thumbnails(channel_name, type_yt):
    channel_url = f"https://www.youtube.com/@{channel_name}/{type_yt}"
    videos_info_file = f"{channel_name} - videos_and_thumbnails_info.json"

    # Create channel directory if it doesn't exist
    create_channel_dirs(channel_name)

    # Extract video information
    channel_info = extract_video_info(channel_url)

    # List to store cleaned video info
    cleaned_video_info = []

    # Process each video for videos and thumbnails
    print(f"Downloading videos and thumbnails from {channel_name}...")

    # Simulate downloading videos and thumbnails
    print("\033[91mDownloading videos and thumbnails:\033[0m ", end="", flush=True)
    for _ in range(10):
        time.sleep(0.2)  # Simulate downloading delay
        print("\033[91m█\033[0m", end="", flush=True)
    print("")

    for video_info in channel_info:
        download_and_save(
            channel_name,
            video_info,
            download_videos=True,
            download_thumbnails=True,
            download_descriptions=False
        )
        cleaned_video_info.append({
            'title': video_info['title'],
            'thumbnail': video_info['thumbnail'],
            'webpage_url': video_info['webpage_url'],
        })

    videos_info_path = os.path.join(channel_name, videos_info_file)
    with open(videos_info_path, 'w', encoding='utf-8') as f:
        json.dump(cleaned_video_info, f, ensure_ascii=False, indent=4)

def print_welcome_message():
    print(logo)
    print("\033[91mWelcome to YouTube Channel archive!\033[0m")

if __name__ == "__main__":
    print_welcome_message()

    channel_name = input("\033[91mEnter the channel name:\033[0m ")
    type_yt = input("\033[91mEnter the type of content (videos or shorts):\033[0m ")

    interactive_menu(channel_name, type_yt)
