import argparse, json, os, sys
import requests
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials

def load_config(path):
    return json.load(open(path,'r',encoding='utf-8'))

def get_credentials_from_refresh(client_id, client_secret, refresh_token):
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token"
    }
    r = requests.post(token_url, data=data)
    r.raise_for_status()
    return r.json()

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--config", required=True)
    args = p.parse_args()
    cfg = load_config(args.config)
    outdir = cfg.get("output_dir","outputs")
    video_path = os.path.join(outdir,"final.mp4")
    if not os.path.exists(video_path):
        print("No video at", video_path); sys.exit(1)

    client_id = os.getenv("YOUTUBE_CLIENT_ID")
    client_secret = os.getenv("YOUTUBE_CLIENT_SECRET")
    refresh_token = os.getenv("YOUTUBE_REFRESH_TOKEN")
    if not (client_id and client_secret and refresh_token):
        print("Missing YouTube credentials."); sys.exit(1)

    token_info = get_credentials_from_refresh(client_id, client_secret, refresh_token)
    access_token = token_info["access_token"]

    creds = Credentials(token=access_token, refresh_token=refresh_token,
                        token_uri="https://oauth2.googleapis.com/token",
                        client_id=client_id, client_secret=client_secret)
    youtube = build("youtube", "v3", credentials=creds)

    body = {
        "snippet": {
            "title": cfg.get("title_template","Creepy Tale"),
            "description": cfg.get("description_template","AI-generated horror story."),
            "tags": ["horror","crime","AI","story"],
            "categoryId": "24"
        },
        "status": {"privacyStatus": "private"}
    }

    media = MediaFileUpload(video_path, chunksize=-1, resumable=True, mimetype='video/mp4')
    req = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
    res = None
    while res is None:
        status, res = req.next_chunk()
        if status:
            print(f"Upload {int(status.progress() * 100)}%")
    print("Upload complete. Video id:", res.get("id"))
