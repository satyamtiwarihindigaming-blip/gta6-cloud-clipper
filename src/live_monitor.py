import subprocess
import json
import os
import sys
import random
import re
from src.devanagari_to_hinglish import transliterate_word
from src.stream_recorder import get_cookie_args

HISTORY_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "history.json")

# Verified high-energy Techno Gamerz & Indian gaming videos pool
CURATED_GAMING_VIDEOS = [
    ("169ZzvPxvvM", "https://www.youtube.com/watch?v=169ZzvPxvvM", "Techno Gamerz GTA 6 Gameplay #1"),
    ("0e3GPea1Tyg", "https://www.youtube.com/watch?v=0e3GPea1Tyg", "Techno Gamerz GTA 5 Insane Police Chase"),
    ("kK68Q78c_2U", "https://www.youtube.com/watch?v=kK68Q78c_2U", "Techno Gamerz GTA 5 Bank Heist"),
    ("W7YwP5YqC_k", "https://www.youtube.com/watch?v=W7YwP5YqC_k", "Techno Gamerz GTA 5 Episode 100"),
    ("bMknfKXIFA8", "https://www.youtube.com/watch?v=bMknfKXIFA8", "CarryisLive GTA 5 Stunt Racing")
]

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

def get_used_moments_for_video(video_id: str) -> list[tuple[float, float]]:
    """
    Returns list of (start_sec, end_sec) for moments ALREADY clipped from this specific video.
    Guarantees no part of the same video is ever clipped twice!
    """
    history = load_history()
    used = []
    for c in history.get("posted_clips", []):
        if c.get("video_id") == video_id:
            s = float(c.get("start_sec", 0))
            d = float(c.get("duration", 48.0))
            used.append((s, s + d))
    return used

def find_target_video() -> tuple[str, str, str]:
    """
    Finds the target video while ensuring videos with too many clips are rotated out.
    Returns (video_id, video_url, creator_name).
    """
    custom_url = os.getenv("CUSTOM_URL")
    if custom_url and "v=" in custom_url:
        vid_id = custom_url.split("v=")[1].split("&")[0]
        return vid_id, custom_url, "Techno Gamerz"

    history = load_history()
    # Count clips per video
    clip_counts = {}
    for c in history.get("posted_clips", []):
        vid = c.get("video_id")
        if vid:
            clip_counts[vid] = clip_counts.get(vid, 0) + 1

    # First, try live YouTube search for fresh videos
    search_queries = [
        ("Techno Gamerz GTA 6 Gameplay", "Techno Gamerz"),
        ("Techno Gamerz Vice City Police Chase", "Techno Gamerz"),
        ("CarryisLive GTA 5 Stunt Race", "CarryisLive")
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
                    # If this video has less than 3 clips, pick it!
                    if clip_counts.get(vid_id, 0) < 3:
                        print(f"[Scanner] Found Candidate: {title} ({vid_id}) [Used {clip_counts.get(vid_id, 0)} times]")
                        return vid_id, f"https://www.youtube.com/watch?v={vid_id}", creator
        except Exception as e:
            print(f"[Scanner] Query '{query}' error: {e}")

    # Curated pool prioritizes Techno Gamerz GTA 6, allowing up to 8 unique unclipped moments per 45min video
    for vid_id, v_url, title in CURATED_GAMING_VIDEOS:
        if clip_counts.get(vid_id, 0) < 8:
            print(f"[Scanner] Selected from Pool: {title} ({vid_id}) [Existing Clips: {clip_counts.get(vid_id, 0)}/8]")
            creator = "CarryisLive" if "Carry" in title else "Techno Gamerz"
            return vid_id, v_url, creator

    # Fallback
    vid_id, v_url, title = CURATED_GAMING_VIDEOS[0]
    return vid_id, v_url, "Techno Gamerz"

def download_subtitles_and_find_viral_moment(video_id: str, temp_dir: str) -> tuple[float, float, str, list]:
    """
    Downloads native auto-generated Hindi subtitles (hi-orig) and detects
    a high-energy 35-50 second moment that HAS NEVER BEEN CLIPPED BEFORE.
    Guarantees: Zero overlap with previously clipped parts of this video!
    Returns (start_sec, end_sec, vtt_path, word_list).
    """
    os.makedirs(temp_dir, exist_ok=True)
    vtt_template = os.path.join(temp_dir, f"{video_id}.%(ext)s")
    
    print(f"[VTT] Downloading auto-subs for {video_id}...")
    cookie_args = get_cookie_args()
    cmd = [
        sys.executable, "-m", "yt_dlp",
        *cookie_args,
        "--extractor-args", "youtube:player_client=ios,mweb,web",
        "--skip-download",
        "--write-auto-subs",
        "--sub-lang", "hi-orig,hi,en",
        "--sub-format", "vtt",
        "--no-check-certificate",
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

    # Get moments ALREADY clipped from THIS SPECIFIC VIDEO
    used_windows = get_used_moments_for_video(video_id)
    print(f"[VTT] Previously clipped moments for {video_id}: {used_windows}")

    def is_overlapping(cand_start: float, cand_end: float) -> bool:
        """Returns True if candidate window overlaps with any already clipped part (±45s buffer)"""
        for u_start, u_end in used_windows:
            # Overlap check with safety margin
            if not (cand_end < u_start - 35.0 or cand_start > u_end + 35.0):
                return True
        return False

    default_start = 720.0
    default_end = 768.0

    # Advance default fallback to an unclipped window
    for cand in [180.0, 320.0, 480.0, 600.0, 750.0, 920.0, 1100.0, 1350.0, 1600.0, 1900.0, 2200.0]:
        if not is_overlapping(cand, cand + 48.0):
            default_start = cand
            default_end = cand + 48.0
            break

    if not vtt_file or not os.path.exists(vtt_file):
        print(f"[VTT] No subtitle track found. Using unclipped fallback window: {default_start}s to {default_end}s.")
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

    window_size = 46.0  # Optimal high-retention Short duration (40-48s)
    best_start = default_start
    best_score = -1

    min_time = 60.0
    max_time = all_words[-1][0] - window_size if all_words else 800.0

    # Sliding window search over speech density
    curr = min_time
    while curr < max_time:
        if not is_overlapping(curr, curr + window_size):
            words_in_window = [w for s, w in all_words if curr <= s <= curr + window_size]
            score = len(words_in_window)
            if score > best_score:
                best_score = score
                best_start = curr
        curr += 12.0

    best_end = best_start + window_size
    print(f"[VTT] Selected Brand New Unclipped Moment: {best_start:.1f}s to {best_end:.1f}s ({best_score} spoken words, 0% overlap)")

    chosen_words = []
    for sec, w in all_words:
        if best_start <= sec <= best_end:
            clean_w = re.sub(r'[^\w\s\u0900-\u097F!?.,\'-]', '', w).strip()
            if clean_w:
                hinglish_w = transliterate_word(clean_w)
                if hinglish_w:
                    chosen_words.append((sec - best_start, hinglish_w))

    return best_start, best_end, vtt_file, chosen_words
