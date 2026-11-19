import subprocess
import os

def record_slice_segment(stream_url: str, output_path: str, start_sec: float, duration: float = 48.0) -> bool:
    """
    Extracts a high-precision 1080p segment using yt-dlp with mobile player client (bypasses bot detection).
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    end_sec = start_sec + duration

    start_m = int(start_sec // 60)
    start_s = int(start_sec % 60)
    end_m = int(end_sec // 60)
    end_s = int(end_sec % 60)

    section_str = f"*{start_m:02d}:{start_s:02d}-{end_m:02d}:{end_s:02d}"
    print(f"[Downloader] Downloading 1080p stream slice ({section_str}) from {stream_url}...")

    # player_client=ios,android avoids datacenter bot-check
    cmd = [
        "yt-dlp",
        "--extractor-args", "youtube:player_client=ios,android",
        "-f", "bestvideo[height<=1080]+bestaudio/best[height<=1080]/best",
        "--download-sections", section_str,
        "--force-keyframes-at-cuts",
        "-o", output_path,
        stream_url
    ]

    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if res.returncode == 0 and os.path.exists(output_path) and os.path.getsize(output_path) > 100000:
            print(f"[Downloader] SUCCESS: Downloaded slice to {output_path} ({os.path.getsize(output_path)} bytes)")
            return True
        else:
            print(f"[Downloader] iOS/Android client error: {res.stderr[-300:]}. Trying fallback...")
            # Fallback with web_creator
            cmd_fb = [
                "yt-dlp",
                "--extractor-args", "youtube:player_client=web_creator,mweb",
                "-f", "bestvideo[height<=1080]+bestaudio/best",
                "--download-sections", section_str,
                "--force-keyframes-at-cuts",
                "-o", output_path,
                stream_url
            ]
            res_fb = subprocess.run(cmd_fb, capture_output=True, text=True, timeout=120)
            if res_fb.returncode == 0 and os.path.exists(output_path) and os.path.getsize(output_path) > 100000:
                print(f"[Downloader] SUCCESS with fallback client: {output_path}")
                return True
            else:
                print(f"[Downloader] Fallback error: {res_fb.stderr[-300:]}")
    except Exception as e:
        print(f"[Downloader] yt-dlp extraction error: {e}")

    return False
