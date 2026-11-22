import subprocess
import os
import sys

def record_slice_segment(stream_url: str, output_path: str, start_sec: float, duration: float = 48.0) -> bool:
    """
    Downloads precision 1080p HD highlight slice using clean yt-dlp with Node/Deno JS runtimes.
    Avoids bot detection by using standard web extractor and POT container sidecar.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    end_sec = start_sec + duration

    start_m = int(start_sec // 60)
    start_s = int(start_sec % 60)
    end_m = int(end_sec // 60)
    end_s = int(end_sec % 60)

    section_str = f"*{start_m:02d}:{start_s:02d}-{end_m:02d}:{end_s:02d}"
    print(f"[Downloader] Downloading 1080p HD stream slice ({section_str}) from {stream_url}...")

    # Strategy 1: Official Node/Deno JS Runtime (Matches working run 44502256730)
    cmd = [
        "yt-dlp",
        "--js-runtimes", "node,deno",
        "-f", "bestvideo[height<=1080]+bestaudio/best[height<=1080]/best",
        "--download-sections", section_str,
        "--force-keyframes-at-cuts",
        "-o", output_path,
        stream_url
    ]

    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
        if res.returncode == 0 and os.path.exists(output_path) and os.path.getsize(output_path) > 100000:
            print(f"[Downloader] SUCCESS: Downloaded 1080p slice to {output_path} ({os.path.getsize(output_path)} bytes)")
            return True
        else:
            print(f"[Downloader] Attempt 1 error: {res.stderr[-300:]}")
    except Exception as e:
        print(f"[Downloader] Attempt 1 exception: {e}")

    # Strategy 2: POT provider container
    cmd_pot = [
        "yt-dlp",
        "--extractor-args", "youtubepot-bgutilhttp:base_url=http://127.0.0.1:4416",
        "--js-runtimes", "node,deno",
        "-f", "bestvideo[height<=1080]+bestaudio/best[height<=1080]/best",
        "--download-sections", section_str,
        "--force-keyframes-at-cuts",
        "-o", output_path,
        stream_url
    ]

    try:
        res = subprocess.run(cmd_pot, capture_output=True, text=True, timeout=180)
        if res.returncode == 0 and os.path.exists(output_path) and os.path.getsize(output_path) > 100000:
            print(f"[Downloader] SUCCESS (POT): Downloaded slice to {output_path} ({os.path.getsize(output_path)} bytes)")
            return True
        else:
            print(f"[Downloader] Attempt 2 error: {res.stderr[-300:]}")
    except Exception as e:
        print(f"[Downloader] Attempt 2 exception: {e}")

    return False
