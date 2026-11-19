import subprocess
import json
import random
from src.config import GTA6_SEARCH_QUERIES

def is_stream_live(streamer_url: str) -> bool:
    """
    Checks if a Twitch or YouTube live stream is actively online using streamlink JSON probe.
    """
    cmd = ["streamlink", "--json", streamer_url]
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, timeout=15)
        if result.returncode == 0 and result.stdout:
            data = json.loads(result.stdout)
            streams = data.get("streams", {})
            return len(streams) > 0
    except Exception as e:
        print(f"Error checking stream status for {streamer_url}: {e}")
    return False

def get_trending_gta6_video() -> tuple[str, str]:
    """
    Finds the latest trending GTA 6 / Streamer video on YouTube as a guaranteed fallback.
    Returns (video_url, title).
    """
    query = random.choice(GTA6_SEARCH_QUERIES)
    print(f"🔍 Searching YouTube for trending clip content: '{query}'...")
    cmd = ["yt-dlp", f"ytsearch1:{query}", "--get-id", "--get-title"]
    try:
        out = subprocess.check_output(cmd, text=True, timeout=30).strip().split("\n")
        if len(out) >= 2:
            title = out[0].strip()
            vid_id = out[1].strip()
            url = f"https://www.youtube.com/watch?v={vid_id}"
            print(f"🎯 Found trending video: {title} ({url})")
            return url, title
    except Exception as e:
        print(f"Search fallback error: {e}")
    
    # Ultimate safe fallback
    return "https://www.youtube.com/watch?v=3PiR0G3rVw8", "GTA 6 Insane Moments"

def find_active_streamer(streamers: list) -> tuple[str, str]:
    """
    Returns (stream_url, creator_name).
    If a target streamer is LIVE, returns their live stream.
    If none are live, returns the latest trending GTA 6 video.
    """
    for streamer in streamers:
        print(f"Checking if {streamer} is LIVE...")
        if is_stream_live(streamer):
            name = streamer.rstrip("/").split("/")[-1].replace("@", "")
            print(f"🎯 FOUND LIVE STREAMER: {name} ({streamer})")
            return streamer, name
            
    print("ℹ️ Target streamers not live right now. Activating GTA 6 Trending Video Pipeline...")
    url, title = get_trending_gta6_video()
    return url, "GTA 6 Gameplay"
