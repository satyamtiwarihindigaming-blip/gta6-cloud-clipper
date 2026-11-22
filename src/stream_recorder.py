import subprocess
import os
import sys

def record_slice_segment(stream_url: str, output_path: str, start_sec: float, duration: float = 48.0) -> bool:
    """
    Extracts a high-precision 1080p HD segment using yt-dlp.
    Guarantees highest available HD quality with multi-client bot-bypass.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    end_sec = start_sec + duration

    start_m = int(start_sec // 60)
    start_s = int(start_sec % 60)
    end_m = int(end_sec // 60)
    end_s = int(end_sec % 60)

    section_str = f"*{start_m:02d}:{start_s:02d}-{end_m:02d}:{end_s:02d}"
    print(f"[Downloader] Downloading 1080p HD stream slice ({section_str}) from {stream_url}...")

    # Strategy 1: Android Client with web fallback
    cmd_android = [
        sys.executable, "-m", "yt_dlp",
        "--extractor-args", "youtube:player_client=android,mweb",
        "-f", "bestvideo[height<=1080]+bestaudio/best[height<=1080]/best",
        "--download-sections", section_str,
        "--force-keyframes-at-cuts",
        "--no-check-certificate",
        "-o", output_path,
        stream_url
    ]

    try:
        print("[Downloader] Attempting download with Android Client (1080p HD)...")
        res = subprocess.run(cmd_android, capture_output=True, text=True, timeout=180)
        if res.returncode == 0 and os.path.exists(output_path) and os.path.getsize(output_path) > 100000:
            print(f"[Downloader] SUCCESS (Android Client): Downloaded HD slice to {output_path} ({os.path.getsize(output_path)} bytes)")
            return True
        else:
            print(f"[Downloader] Android attempt returned {res.returncode}. Stderr: {res.stderr[-300:]}")
    except Exception as e:
        print(f"[Downloader] Android attempt exception: {e}")

    # Strategy 2: POT provider with mweb/web
    print("[Downloader] Attempting Fallback Strategy 2: POT provider...")
    cmd_pot = [
        sys.executable, "-m", "yt_dlp",
        "--extractor-args", "youtubepot-bgutilhttp:base_url=http://127.0.0.1:4416",
        "--extractor-args", "youtube:player_client=mweb,web",
        "-f", "bestvideo[height<=1080]+bestaudio/best[height<=1080]/best",
        "--download-sections", section_str,
        "--force-keyframes-at-cuts",
        "--no-check-certificate",
        "-o", output_path,
        stream_url
    ]

    try:
        res = subprocess.run(cmd_pot, capture_output=True, text=True, timeout=180)
        if res.returncode == 0 and os.path.exists(output_path) and os.path.getsize(output_path) > 100000:
            print(f"[Downloader] SUCCESS (POT Fallback): Downloaded slice to {output_path} ({os.path.getsize(output_path)} bytes)")
            return True
        else:
            print(f"[Downloader] POT attempt error: {res.stderr[-300:]}")
    except Exception as e:
        print(f"[Downloader] POT attempt exception: {e}")

    # Strategy 3: Standard best client
    print("[Downloader] Attempting Fallback Strategy 3: Standard Client...")
    cmd_std = [
        sys.executable, "-m", "yt_dlp",
        "-f", "bestvideo[height<=1080]+bestaudio/best[height<=1080]/best",
        "--download-sections", section_str,
        "--force-keyframes-at-cuts",
        "--no-check-certificate",
        "-o", output_path,
        stream_url
    ]

    try:
        res = subprocess.run(cmd_std, capture_output=True, text=True, timeout=180)
        if res.returncode == 0 and os.path.exists(output_path) and os.path.getsize(output_path) > 100000:
            print(f"[Downloader] SUCCESS (Standard Client): Downloaded slice to {output_path} ({os.path.getsize(output_path)} bytes)")
            return True
        else:
            print(f"[Downloader] Standard attempt error: {res.stderr[-300:]}")
    except Exception as e:
        print(f"[Downloader] Standard attempt exception: {e}")

    return False
