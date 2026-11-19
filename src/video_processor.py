import os
import subprocess
from src.word_captions import generate_word_by_word_ass

def get_creator_crops(creator_name: str) -> tuple[str, str]:
    c_lower = creator_name.lower()
    if "techno" in c_lower or "ujjwalgamer" in c_lower or "technogamerz" in c_lower:
        # Techno Gamerz crystal-clear HD facecam crop (Lanczos + Unsharp, zero blur)
        top_crop = "scale=1920:1080,crop=300:266:1565:80,scale=1080:960:flags=lanczos,unsharp=5:5:1.2:5:5:0.0"
        bot_crop = "scale=1920:1080,crop=1205:1070:350:0,scale=1080:960:flags=lanczos"
    elif "carry" in c_lower:
        # CarryisLive HD crop
        top_crop = "scale=1920:1080,crop=330:300:1580:750,scale=1080:960:flags=lanczos,unsharp=5:5:1.2:5:5:0.0"
        bot_crop = "scale=1920:1080,crop=1280:720:0:0,scale=1080:960:flags=lanczos"
    elif "insaan" in c_lower or "triggered" in c_lower:
        # Triggered Insaan / Live Insaan crop
        top_crop = "scale=1920:1080,crop=400:350:1500:700,scale=1080:960:flags=lanczos,unsharp=5:5:1.2:5:5:0.0"
        bot_crop = "scale=1920:1080,crop=1280:720:0:0,scale=1080:960:flags=lanczos"
    else:
        # Universal clean gaming split
        top_crop = "scale=1920:1080,crop=in_w*0.45:in_h*0.5:in_w*0.55:0,scale=1080:960:flags=lanczos,unsharp=5:5:1.2:5:5:0.0"
        bot_crop = "scale=1920:1080,crop=in_w*0.8:in_h*0.8:in_w*0.1:in_h*0.1,scale=1080:960:flags=lanczos"

    return top_crop, bot_crop

def convert_to_vertical_short(
    input_path: str,
    output_path: str,
    creator_name: str = "Techno Gamerz",
    word_list: list = None,
    duration: float = 48.0
) -> bool:
    """
    Renders 1080x1920 (9:16 Vertical HD) 60 FPS Short/Reel with:
    - Top: Streamer Facecam (1080x960, Lanczos + Unsharp, ZERO blur)
    - Bottom: Gameplay (1080x960)
    - Middle: 100% CLEAN SPLIT (Zero text/badges/separators)
    - Captions: Word-by-word dynamic popping in Hinglish (Roman script, zero emojis, silence VAD)
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    temp_dir = os.path.dirname(output_path)

    ass_path = os.path.join(temp_dir, "speech_word_by_word.ass")
    generate_word_by_word_ass(ass_path, word_list or [], total_duration=duration)

    ass_escaped = ass_path.replace("\\", "/").replace(":", "\\:")
    top_crop, bot_crop = get_creator_crops(creator_name)

    if os.path.exists(ass_path) and os.path.getsize(ass_path) > 300:
        filter_complex = (
            f"[0:v]{top_crop}[top];"
            f"[0:v]{bot_crop}[bot];"
            f"[top][bot]vstack[vstacked];"
            f"[vstacked]ass='{ass_escaped}'[vout];"
            f"[0:a]loudnorm=I=-14:LRA=7:tp=-1[aout]"
        )
    else:
        filter_complex = (
            f"[0:v]{top_crop}[top];"
            f"[0:v]{bot_crop}[bot];"
            f"[top][bot]vstack[vout];"
            f"[0:a]loudnorm=I=-14:LRA=7:tp=-1[aout]"
        )

    cmd = [
        "ffmpeg", "-y",
        "-avoid_negative_ts", "make_zero",
        "-i", input_path,
        "-filter_complex", filter_complex,
        "-map", "[vout]",
        "-map", "[aout]",
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "18",
        "-r", "60",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "160k",
        "-t", str(duration),
        output_path
    ]

    print(f"[FFmpeg] Rendering 1080x1920 60FPS Short for {creator_name}...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0 and os.path.exists(output_path):
        size_mb = os.path.getsize(output_path) / (1024 * 1024)
        print(f"[FFmpeg] SUCCESS: Rendered {output_path} ({size_mb:.2f} MB, 60fps HD Lossless)")
        return True
    else:
        print(f"[FFmpeg] Error: {res.stderr[-500:]}")
        return False
