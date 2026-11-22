import subprocess
import os
import sys

def get_cookie_args():
    """Returns --cookies flag if cookies.txt exists and is valid."""
    for candidate in ["cookies.txt", "youtube_cookies.txt"]:
        if os.path.exists(candidate) and os.path.getsize(candidate) > 50:
            return ["--cookies", candidate]
    return []

def record_slice_segment(stream_url: str, output_path: str, start_sec: float, duration: float = 48.0) -> bool:
    """
    Downloads precision 1080p HD highlight slice using python -m yt_dlp.
    Tries multiple client architectures (iOS, POT Web, mWeb, TV).
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

    strategies = [
        ("iOS Client (Datacenter-friendly)", [
            "--extractor-args", "youtube:player_client=ios",
            "-f", "bestvideo[height<=1080]+bestaudio/best[height<=1080]/best"
        ]),
        ("POT Provider Sidecar (Web Client)", [
            "--extractor-args", "youtubepot-bgutilhttp:base_url=http://127.0.0.1:4416",
            "--extractor-args", "youtube:player_client=web",
            "--js-runtimes", "deno",
            "-f", "bestvideo[height<=1080]+bestaudio/best[height<=1080]/best"
        ]),
        ("Mobile Web & Android Client", [
            "--extractor-args", "youtube:player_client=mweb,android",
            "-f", "bestvideo[height<=1080]+bestaudio/best[height<=1080]/best"
        ]),
        ("TV & Web Embedded Client", [
            "--extractor-args", "youtube:player_client=tv,web_embedded;player_skip=webpage",
            "-f", "bestvideo[height<=1080]+bestaudio/best[height<=1080]/best"
        ]),
        ("Fallback Single Format MP4 (Format 18)", [
            "--extractor-args", "youtube:player_client=ios,tv",
            "-f", "18/best[ext=mp4]/best"
        ])
    ]

    for name, extra_args in strategies:
        cmd = [
            sys.executable, "-m", "yt_dlp",
            *cookie_args,
            *extra_args,
            "--download-sections", section_str,
            "--force-keyframes-at-cuts",
            "--merge-output-format", "mp4",
            "--no-check-certificate",
            "-o", out_template,
            stream_url
        ]
        try:
            print(f"[Downloader] Trying: {name}...")
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
            if os.path.exists(target_mp4) and os.path.getsize(target_mp4) > 100000:
                print(f"[Downloader] SUCCESS ({name}): Downloaded slice to {target_mp4} ({os.path.getsize(target_mp4)} bytes)")
                if target_mp4 != output_path:
                    os.replace(target_mp4, output_path)
                return True
            else:
                err_snippet = res.stderr[-200:].replace('\n', ' ') if res.stderr else "No output"
                print(f"[Downloader] {name} failed: {err_snippet}")
        except Exception as e:
            print(f"[Downloader] {name} exception: {e}")

    return False
