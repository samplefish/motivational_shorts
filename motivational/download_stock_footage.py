import os
import requests
import json
import glob

def download_videos():
    pexels_api_key = os.getenv("pexels_api_key")
    PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

    SEARCH_QUERY = "athlete"  
    NUM_VIDEOS = 3
    OUTPUT_DIR = "motivational/stock_footage"
    MEMORY_FILE = "downloaded_ids.txt"

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            downloaded_ids = set(line.strip() for line in f)
    else:
        downloaded_ids = set()

    for file in glob.glob(os.path.join(OUTPUT_DIR, "*.mp4")):
        os.remove(file)
        print(f"Deleted old file: {file}")

    headers = {"Authorization": PEXELS_API_KEY}
    base_url = "https://api.pexels.com/videos/search"
    params = {"query": SEARCH_QUERY, "per_page": NUM_VIDEOS, "orientation": "portrait"}

    # response = requests.get(url, headers=headers, params=params)
    # data = response.json()


    new_ids = []
    page = 1

    while len(new_ids) < NUM_VIDEOS:
        params = {
            "query": SEARCH_QUERY,
            "per_page": NUM_VIDEOS*2, 
            "orientation": "portrait",
            "page": page,
        }

        response = requests.get(base_url, headers=headers, params=params)
        data = response.json()

        videos = data.get("videos", [])
        if not videos:
            print("Cant find videos")
            break

        for video in videos:
            vid_id = str(video["id"])
            if vid_id in downloaded_ids or vid_id in new_ids:
                continue

            video_url = video["video_files"][0]["link"]
            filename = os.path.join(OUTPUT_DIR, f"pexels_{vid_id}.mp4")

            print(f"Downloading {video_url} -> {filename}")
            vid_data = requests.get(video_url)
            with open(filename, "wb") as f:
                f.write(vid_data.content)

            new_ids.append(vid_id)
            if len(new_ids) >= NUM_VIDEOS:
                break

        page += 1

    with open(MEMORY_FILE, "a") as f:
        for vid_id in new_ids:
            f.write(vid_id + "\n")

    print(f"Downloaded {len(new_ids)} new videos")