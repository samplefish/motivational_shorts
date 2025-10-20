import os
import google.auth.transport.requests
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import pickle
from google.auth.transport.requests import Request

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

# def get_youtube_service():
#     flow = InstalledAppFlow.from_client_secrets_file(
#         "client_secret_605218052235-nnpstmsvfeuv9dt1cgcf33fntoita5bt.apps.googleusercontent.com.json", SCOPES
#     )
#     creds = flow.run_local_server(port=8080)
#     return build("youtube", "v3", credentials=creds)

def get_youtube_service():
    creds = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "client_secret_605218052235-nnpstmsvfeuv9dt1cgcf33fntoita5bt.apps.googleusercontent.com.json", SCOPES
            )
            creds = flow.run_local_server(port=8080)

        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    return build("youtube", "v3", credentials=creds)

def upload_video(file_path, title, description, category="22", privacy="private"):
    youtube = get_youtube_service()

    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": ["cat", "funny", "shorts"]
        },
        "status": {
            "privacyStatus": privacy
        }
    }

    media = MediaFileUpload(file_path, chunksize=-1, resumable=True)

    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media
    )
    response = request.execute()
    print("Upload success, video id:", response["id"])
