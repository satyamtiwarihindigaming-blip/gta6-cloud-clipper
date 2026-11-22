import subprocess
import os
import sys

def record_slice_segment(stream_url: str, output_path: str, start_sec: float, duration: float = 48.0) -> bool:
    """
    Downloads precision 1080p HD highlight slice using python -m yt_dlp with Deno JS runtime.
    Uses bgutil-ytdlp-pot-provider sidecar and multi-client fallback (web, ios, mweb).
    Uses %(ext)s template + merge-output-format to merge separate audio/video streams cleanly.
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

    # Strategy 1: Deno JS Runtime + POT sidecar + Web/iOS client fallback
    cmd = [
        sys.executable, "-m", "yt_dlp",
        "--js-runtimes", "deno",
        "--extractor-args", "youtubepot-bgutilhttp:base_url=http://127.0.0.1:4416",
        "--extractor-args", "youtube:player_client=web,ios,mweb",
        "-f", "bestvideo[height<=1080]+bestaudio/best[height<=1080]/best",
        "--download-sections", section_str,
        "--force-keyframes-at-cuts",
        "--merge-output-format", "mp4",
        "--no-check-certificate",
        "-o", out_template,
        stream_url
    ]

    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
        # Check if output_path or base_no_ext.mp4 exists
        target_mp4 = f"{base_no_ext}.mp4"
        if os.path.exists(target_mp4) and os.path.getsize(target_mp4) > 100000:
            print(f"[Downloader] SUCCESS: Downloaded 1080p slice to {target_mp4} ({os.path.getsize(target_mp4)} bytes)")
            if target_mp4 != output_path:
                os.replace(target_mp4, output_path)
            return True
        else:
            print(f"[Downloader] Attempt 1 error: {res.stderr[-300:]}")
    except Exception as e:
        print(f"[Downloader] Attempt 1 exception: {e}")

    # Strategy 2: Direct iOS Client fallback
    cmd_ios = [
        sys.executable, "-m", "yt_dlp",
        "--extractor-args", "youtube:player_client=ios",
        "-f", "bestvideo[height<=1080]+bestaudio/best[height<=1080]/best",
        "--download-sections", section_str,
        "--force-keyframes-at-cuts",
        "--merge-output-format", "mp4",
        "--no-check-certificate",
        "-o", out_template,
        stream_url
    ]

    try:
        res = subprocess.run(cmd_ios, capture_output=True, text=True, timeout=180)
        target_mp4 = f"{base_no_ext}.mp4"
        if os.path.exists(target_mp4) and os.path.getsize(target_mp4) > 100000:
            print(f"[Downloader] SUCCESS (iOS Client): Downloaded slice to {target_mp4} ({os.path.getsize(target_mp4)} bytes)")
            if target_mp4 != output_path:
                os.replace(target_mp4, output_path)
            return True
        else:
            print(f"[Downloader] Attempt 2 error: {res.stderr[-300:]}")
    except Exception as e:
        print(f"[Downloader] Attempt 2 exception: {e}")

    return False
