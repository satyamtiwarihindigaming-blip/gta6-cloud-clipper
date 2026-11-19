import subprocess
import os
import sys

def record_slice_segment(stream_url: str, output_path: str, start_sec: float, duration: float = 48.0) -> bool:
    """
    Extracts a high-precision segment using yt-dlp with bgutil POT provider & resilient player clients.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    end_sec = start_sec + duration

    start_m = int(start_sec // 60)
    start_s = int(start_sec % 60)
    end_m = int(end_sec // 60)
    end_s = int(end_sec % 60)

    section_str = f"*{start_m:02d}:{start_s:02d}-{end_m:02d}:{end_s:02d}"
    print(f"[Downloader] Downloading stream slice ({section_str}) from {stream_url}...")

    # Strategy 1: Primary 1080p using POT provider (mweb, web)
    cmd_primary = [
        sys.executable, "-m", "yt_dlp",
        "--extractor-args", "youtubepot-bgutilhttp:base_url=http://127.0.0.1:4416",
        "--extractor-args", "youtube:player_client=mweb,web",
        "-f", "bestvideo[height<=1080]+bestaudio/best[height<=1080]/best/18",
        "--download-sections", section_str,
        "--force-keyframes-at-cuts",
        "-o", output_path,
        stream_url
    ]

    try:
        res = subprocess.run(cmd_primary, capture_output=True, text=True, timeout=180)
        if res.returncode == 0 and os.path.exists(output_path) and os.path.getsize(output_path) > 100000:
            print(f"[Downloader] SUCCESS (POT Primary): Downloaded slice to {output_path} ({os.path.getsize(output_path)} bytes)")
            return True
        else:
            print(f"[Downloader] Primary attempt returned {res.returncode}. Stderr: {res.stderr[-300:]}")
    except Exception as e:
        print(f"[Downloader] Primary attempt exception: {e}")

    # Strategy 2: Resilient Android client fallback (bypasses web bot checks without POT)
    print("[Downloader] Attempting Fallback Strategy 2: Android Player Client...")
    cmd_fallback = [
        sys.executable, "-m", "yt_dlp",
        "--extractor-args", "youtube:player_client=android",
        "-f", "bestvideo[height<=1080]+bestaudio/best[height<=1080]/best/18",
        "--download-sections", section_str,
        "--force-keyframes-at-cuts",
        "-o", output_path,
        stream_url
    ]

    try:
        res = subprocess.run(cmd_fallback, capture_output=True, text=True, timeout=180)
        if res.returncode == 0 and os.path.exists(output_path) and os.path.getsize(output_path) > 100000:
            print(f"[Downloader] SUCCESS (Android Fallback): Downloaded slice to {output_path} ({os.path.getsize(output_path)} bytes)")
            return True
        else:
            print(f"[Downloader] Fallback attempt error: {res.stderr[-300:]}")
    except Exception as e:
        print(f"[Downloader] Fallback attempt exception: {e}")

    # Strategy 3: Standard yt-dlp fallback
    print("[Downloader] Attempting Fallback Strategy 3: Default client...")
    cmd_default = [
        "yt-dlp",
        "-f", "bestvideo[height<=1080]+bestaudio/best[height<=1080]/best/18",
        "--download-sections", section_str,
        "--force-keyframes-at-cuts",
        "-o", output_path,
        stream_url
    ]

    try:
        res = subprocess.run(cmd_default, capture_output=True, text=True, timeout=180)
        if res.returncode == 0 and os.path.exists(output_path) and os.path.getsize(output_path) > 100000:
            print(f"[Downloader] SUCCESS (Default Fallback): Downloaded slice to {output_path} ({os.path.getsize(output_path)} bytes)")
            return True
        else:
            print(f"[Downloader] Final fallback error: {res.stderr[-300:]}")
    except Exception as e:
        print(f"[Downloader] Final fallback exception: {e}")

    return False
