import subprocess
import json
import os
import sys
import random
import re

HISTORY_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "history.json")

def load_history() -> dict:
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"posted_clips": [], "processed_moments": []}

def save_history(history: dict):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)

def find_target_video() -> tuple[str, str, str]:
    """
    Finds the latest Techno Gamerz GTA 6 video/stream or top Indian creator video.
    Returns (video_id, video_url, creator_name).
    """
    custom_url = os.getenv("CUSTOM_URL")
    if custom_url and "v=" in custom_url:
        vid_id = custom_url.split("v=")[1].split("&")[0]
        return vid_id, custom_url, "Techno Gamerz"

    search_queries = [
        ("Techno Gamerz GTA 6 Gameplay", "Techno Gamerz"),
        ("Techno Gamerz Vice City Police Chase", "Techno Gamerz"),
        ("CarryisLive GTA 5 Stunt Race", "CarryisLive"),
        ("Live Insaan GTA 5 Funny Moments", "Live Insaan")
    ]

    for query, creator in search_queries:
        print(f"[Scanner] Searching YouTube for: '{query}'...")
        cmd = [
            sys.executable, "-m", "yt_dlp",
            "--extractor-args", "youtube:player_client=android,web",
            f"ytsearch5:{query}",
            "--get-id",
            "--get-title"
        ]
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=35)
            lines = [l.strip() for l in res.stdout.strip().split("\n") if l.strip()]
            for i in range(0, len(lines) - 1, 2):
                title = lines[i]
                vid_id = lines[i + 1]
                if len(vid_id) == 11:
                    print(f"[Scanner] Found Candidate: {title} ({vid_id}) by {creator}")
                    return vid_id, f"https://www.youtube.com/watch?v={vid_id}", creator
        except Exception as e:
            print(f"[Scanner] Query '{query}' failed: {e}")

    # Fallback to verified Techno Gamerz GTA 6 video
    return "169ZzvPxvvM", "https://www.youtube.com/watch?v=169ZzvPxvvM", "Techno Gamerz"

def download_subtitles_and_find_viral_moment(video_id: str, temp_dir: str) -> tuple[float, float, str, list]:
    """
    Downloads native auto-generated Hindi subtitles (hi-orig) and detects
    a high-energy 45-55 second moment that hasn't been clipped yet.
    Returns (start_sec, end_sec, vtt_path, word_list).
    """
    os.makedirs(temp_dir, exist_ok=True)
    vtt_template = os.path.join(temp_dir, f"{video_id}.%(ext)s")
    
    print(f"[VTT] Downloading auto-subs for {video_id}...")
    cmd = [
        sys.executable, "-m", "yt_dlp",
        "--extractor-args", "youtubepot-bgutilhttp:base_url=http://127.0.0.1:4416",
        "--extractor-args", "youtube:player_client=mweb,android,web",
        "--skip-download",
        "--write-auto-subs",
        "--sub-lang", "hi-orig,hi,en",
        "--sub-format", "vtt",
        "-o", vtt_template,
        f"https://www.youtube.com/watch?v={video_id}"
    ]
    try:
        subprocess.run(cmd, capture_output=True, text=True, timeout=40)
    except Exception as e:
        print(f"[VTT] Subtitle fetch error: {e}")

    # Find the downloaded vtt file
    vtt_file = None
    for f in os.listdir(temp_dir):
        if f.startswith(video_id) and f.endswith(".vtt"):
            vtt_file = os.path.join(temp_dir, f)
            break

    history = load_history()
    used_moments = history.get("processed_moments", [])

    default_start = 720.0
    default_end = 768.0

    # Advance fallback to next unclipped moment if needed
    for cand in [720.0, 840.0, 960.0, 1100.0, 1350.0, 1600.0, 1900.0, 2200.0]:
        if not any(abs(cand - m) < 50 for m in used_moments if m):
            default_start = cand
            default_end = cand + 48.0
            break

    if not vtt_file or not os.path.exists(vtt_file):
        print(f"[VTT] No subtitle track found. Using high-action fallback window: {default_start}s to {default_end}s.")
        return default_start, default_end, None, []

    from src.word_captions import to_sec
    with open(vtt_file, "r", encoding="utf-8", errors="ignore") as f:
        vtt_content = f.read()

    matches = list(re.finditer(r'<(\d{2}:\d{2}:\d{2}\.\d{3})><c>\s*([^<]+)</c>', vtt_content))
    if len(matches) < 20:
        return default_start, default_end, vtt_file, []

    all_words = []
    for m in matches:
        sec = to_sec(m.group(1))
        w = m.group(2).strip()
        if w:
            all_words.append((sec, w))

    window_size = 48.0
    best_start = default_start
    best_score = -1

    min_time = 120.0
    max_time = all_words[-1][0] - window_size if all_words else 800.0

    curr = min_time
    while curr < max_time:
        overlap = any(abs(curr - m_start) < 40 for m_start in used_moments if m_start)
        if not overlap:
            words_in_window = [w for s, w in all_words if curr <= s <= curr + window_size]
            score = len(words_in_window)
            if score > best_score:
                best_score = score
                best_start = curr
        curr += 15.0

    best_end = best_start + window_size
    print(f"[VTT] Selected Best Viral Speech Window: {best_start:.1f}s to {best_end:.1f}s ({best_score} spoken words)")

    chosen_words = []
    for sec, w in all_words:
        if best_start <= sec <= best_end:
            clean_w = re.sub(r'[^\w\s\u0900-\u097F!?.,\'-]', '', w).strip().upper()
            if clean_w:
                chosen_words.append((sec - best_start, clean_w))

    return best_start, best_end, vtt_file, chosen_words
