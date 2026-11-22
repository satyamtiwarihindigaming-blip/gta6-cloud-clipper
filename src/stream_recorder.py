import subprocess
import os
import sys

def get_cookie_args():
    """Returns --cookies flag if cookies.txt exists and is valid."""
    for candidate in ["cookies.txt", "/etc/yt-dlp-cookies.txt", "youtube_cookies.txt"]:
        if os.path.exists(candidate) and os.path.getsize(candidate) > 50:
            return ["--cookies", candidate]
    return []

def record_slice_segment(stream_url: str, output_path: str, start_sec: float, duration: float = 48.0) -> bool:
    """
    Downloads precision 1080p HD highlight slice using python -m yt_dlp.
    Uses TV & web_embedded clients with player_skip=webpage to bypass datacenter IP restrictions.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    end_sec = start_sec + duration

    start_m = int(start_sec // 60)
    start_s = int(start_sec % 60)
    end_m = int(end_sec // 60)
    end_s = int(end_sec % 60)

    section_str = f"*{start_m:02d}:{start_s:02d}-{end_m:02d}:{end_s:02d}"
    print(f"[Downloader] Downloading 1080p HD stream slice ({section_str}) from {stream_url}...")

    base_no_ext = os.path.splitext(output_path)[0]
    out_template = f"{base_no_ext}.%(ext)s"
    target_mp4 = f"{base_no_ext}.mp4"
    cookie_args = get_cookie_args()
    if cookie_args:
        print(f"[Downloader] Using cookies: {cookie_args[1]}")

    # Strategy 1: TV & Web_Embedded client with webpage skip (Known cloud datacenter bypass)
    cmd_tv = [
        sys.executable, "-m", "yt_dlp",
        *cookie_args,
        "--extractor-args", "youtube:player_client=tv,web_embedded;player_skip=webpage",
        "-f", "bestvideo[height<=1080]+bestaudio/best[height<=1080]/best",
        "--download-sections", section_str,
        "--force-keyframes-at-cuts",
        "--merge-output-format", "mp4",
        "--no-check-certificate",
        "-o", out_template,
        stream_url
    ]

    try:
        print("[Downloader] Strategy 1: TV & Web Embedded client...")
        res = subprocess.run(cmd_tv, capture_output=True, text=True, timeout=180)
        if os.path.exists(target_mp4) and os.path.getsize(target_mp4) > 100000:
            print(f"[Downloader] SUCCESS (TV/Embedded): Downloaded slice to {target_mp4} ({os.path.getsize(target_mp4)} bytes)")
            if target_mp4 != output_path:
                os.replace(target_mp4, output_path)
            return True
        else:
            print(f"[Downloader] Strategy 1 error: {res.stderr[-300:]}")
    except Exception as e:
        print(f"[Downloader] Strategy 1 exception: {e}")

    # Strategy 2: POT provider sidecar
    cmd_pot = [
        sys.executable, "-m", "yt_dlp",
        *cookie_args,
        "--extractor-args", "youtubepot-bgutilhttp:base_url=http://127.0.0.1:4416",
        "--js-runtimes", "deno",
        "-f", "bestvideo[height<=1080]+bestaudio/best[height<=1080]/best",
        "--download-sections", section_str,
        "--force-keyframes-at-cuts",
        "--merge-output-format", "mp4",
        "--no-check-certificate",
        "-o", out_template,
        stream_url
    ]

    try:
        print("[Downloader] Strategy 2: POT provider container...")
        res = subprocess.run(cmd_pot, capture_output=True, text=True, timeout=180)
        if os.path.exists(target_mp4) and os.path.getsize(target_mp4) > 100000:
            print(f"[Downloader] SUCCESS (POT sidecar): Downloaded slice to {target_mp4} ({os.path.getsize(target_mp4)} bytes)")
            if target_mp4 != output_path:
                os.replace(target_mp4, output_path)
            return True
        else:
            print(f"[Downloader] Strategy 2 error: {res.stderr[-300:]}")
    except Exception as e:
        print(f"[Downloader] Strategy 2 exception: {e}")

    # Strategy 3: Single format MP4 (18)
    cmd_single = [
        sys.executable, "-m", "yt_dlp",
        *cookie_args,
        "--extractor-args", "youtube:player_client=tv,web_embedded",
        "-f", "18/best[ext=mp4]/best",
        "--download-sections", section_str,
        "--force-keyframes-at-cuts",
        "--no-check-certificate",
        "-o", out_template,
        stream_url
    ]

    try:
        print("[Downloader] Strategy 3: Single format MP4...")
        res = subprocess.run(cmd_single, capture_output=True, text=True, timeout=180)
        if os.path.exists(target_mp4) and os.path.getsize(target_mp4) > 100000:
            print(f"[Downloader] SUCCESS (Single format): Downloaded slice to {target_mp4} ({os.path.getsize(target_mp4)} bytes)")
            if target_mp4 != output_path:
                os.replace(target_mp4, output_path)
            return True
        else:
            print(f"[Downloader] Strategy 3 error: {res.stderr[-300:]}")
    except Exception as e:
        print(f"[Downloader] Strategy 3 exception: {e}")

    return False
