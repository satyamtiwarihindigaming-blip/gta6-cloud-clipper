import subprocess
import os

def record_slice_segment(stream_url: str, output_path: str, start_sec: float, duration: float = 48.0) -> bool:
    """
    Extracts a high-precision 1080p segment using yt-dlp download sections.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    end_sec = start_sec + duration

    start_m = int(start_sec // 60)
    start_s = int(start_sec % 60)
    end_m = int(end_sec // 60)
    end_s = int(end_sec % 60)

    section_str = f"*{start_m:02d}:{start_s:02d}-{end_m:02d}:{end_s:02d}"
    print(f"[Downloader] Downloading 1080p stream slice ({section_str}) from {stream_url}...")

    cmd = [
        "yt-dlp",
        "--js-runtimes", "node",
        "-f", "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
        "--download-sections", section_str,
        "--force-keyframes-at-cuts",
        "-o", output_path,
        stream_url
    ]

    try:
        subprocess.run(cmd, check=True, timeout=120)
        if os.path.exists(output_path) and os.path.getsize(output_path) > 100000:
            print(f"[Downloader] SUCCESS: Downloaded slice to {output_path} ({os.path.getsize(output_path)} bytes)")
            return True
    except Exception as e:
        print(f"[Downloader] yt-dlp extraction error: {e}")

    return False
