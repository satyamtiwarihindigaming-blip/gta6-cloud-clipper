import os
from src.youtube_uploader import upload_short_to_youtube
from src.buffer_uploader import upload_reel_to_buffer

def upload_to_socials(video_path: str, meta: dict) -> dict:
    results = {}

    # 1. YouTube Shorts Upload
    yt_title = meta.get("yt_title", "GTA 6 Viral Moment #shorts")
    yt_desc = meta.get("yt_desc", "")
    yt_tags = meta.get("yt_tags", [])
    
    print(f"\n[Socials] 1. Publishing to YouTube Shorts: '{yt_title}'...")
    yt_url = upload_short_to_youtube(video_path, yt_title, yt_desc, yt_tags)
    results["youtube_url"] = yt_url or "failed"

    # 2. Instagram Reels Upload via Buffer
    ig_caption = meta.get("ig_caption", "")
    print(f"\n[Socials] 2. Publishing to Instagram Reels (@grow10z) via Buffer...")
    ig_success = upload_reel_to_buffer(video_path, ig_caption)
    results["instagram_success"] = ig_success

    return results
