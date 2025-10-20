from motivational import upload_motivation, download_stock_footage, motivation
import json
import re
import argparse

def first_sentence(text: str) -> str:
    match = re.match(r'^(.*?\.)', text)
    return match.group(1) if match else text

def main():
    with open("motivational\\quotes\\quotes.json", "r", encoding="utf-8") as f:
        scripts = json.load(f)

    parser = argparse.ArgumentParser(description="Create a motivational short.")
    parser.add_argument("--rdl", type=str, default=1, help="Redownload stock footage")
    parser.add_argument("--upl", type=str, default=1, help="Upload video")
    args = parser.parse_args()
    redownload_flag = args.rdl
    upload_flag = args.upl

    if args.rdl == 1:
        download_stock_footage.download_videos()

    for script in scripts:
        motivation.create_short(script["script"])
        fs = first_sentence(script["script"])
        if upload_flag:
            upload_motivation.upload_video(
                "motivational_short.mp4", 
                fs,  # title
                fs,  # description
                privacy="public" 
            )

if __name__ == "__main__":
    main()
