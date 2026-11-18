import subprocess
import json

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

def find_active_streamer(streamers: list) -> str:
    """
    Iterates through the target streamers list and returns the first active one.
    """
    for streamer in streamers:
        print(f"Checking if {streamer} is LIVE...")
        if is_stream_live(streamer):
            print(f"🎯 FOUND LIVE STREAMER: {streamer}")
            return streamer
    print("No target streamers are currently live.")
    return None
