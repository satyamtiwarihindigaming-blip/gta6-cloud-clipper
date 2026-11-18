import os
import requests
from src.youtube_uploader import upload_short_to_youtube

def upload_to_socials(video_path: str, title: str, description: str, tags: str) -> bool:
    print(f"Publishing: '{title}'...")
    
    yt_url = upload_short_to_youtube(video_path, title, description, tags)
    if yt_url:
        print(f"[YouTube] Shorts LIVE: {yt_url}")
    
    webhook_url = os.getenv("SOCIAL_WEBHOOK_URL")
    if webhook_url:
        try:
            payload = {
                "title": title,
                "description": f"{description}\n\n{tags}",
                "tags": tags,
                "youtube_url": yt_url or ""
            }
            requests.post(webhook_url, json=payload, timeout=15)
            print("Webhook triggered for automated social posting!")
        except Exception as e:
            print(f"Social webhook upload error: {e}")

    return True
