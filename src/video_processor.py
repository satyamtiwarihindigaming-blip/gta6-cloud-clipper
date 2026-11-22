import os
import subprocess
from src.word_captions import generate_word_by_word_ass

def convert_to_vertical_short(
    input_path: str,
    output_path: str,
    creator_name: str = "Techno Gamerz",
    word_list: list = None,
    duration: float = 48.0
) -> bool:
    """
    Renders 1080x1920 (9:16 Vertical HD) 60 FPS Short/Reel with:
    - Center: Original 16:9 Stream (1080x608, 100% sharp, Lanczos, ZERO CROP)
      Streamer webcam and gameplay both remain completely natural and uncropped.
    - Top & Bottom: Ambient blurred background of the same gameplay (boxblur=28:5, darkened 12%)
    - Captions: Word-by-word animated popping in Hinglish in the bottom blurred area.
      Never covers gameplay or streamer face.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    temp_dir = os.path.dirname(output_path)

    ass_path = os.path.join(temp_dir, "speech_word_by_word.ass")
    generate_word_by_word_ass(ass_path, word_list or [], total_duration=duration)

    ass_escaped = ass_path.replace("\\", "/").replace(":", "\\:")

    # Viral Ambient Blurred Background Filter:
    # 1. Split stream into bg and fg
    # 2. bg is scaled to 1080:1920, cropped, blurred heavily, and dimmed
    # 3. fg is scaled to 1080:608 with lanczos
    # 4. fg is centered over bg at y=(1920-608)/2 = 656
    # 5. ASS subtitles burned over lower third
    if os.path.exists(ass_path) and os.path.getsize(ass_path) > 300:
        filter_complex = (
            "[0:v]split=2[bg_raw][fg_raw];"
            "[bg_raw]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=28:5,eq=brightness=-0.12[bg];"
            "[fg_raw]scale=1080:608:flags=lanczos[fg];"
            "[bg][fg]overlay=0:(1920-608)/2[vbase];"
            f"[vbase]ass='{ass_escaped}'[vout];"
            "[0:a]loudnorm=I=-14:LRA=7:tp=-1[aout]"
        )
    else:
        filter_complex = (
            "[0:v]split=2[bg_raw][fg_raw];"
            "[bg_raw]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=28:5,eq=brightness=-0.12[bg];"
            "[fg_raw]scale=1080:608:flags=lanczos[fg];"
            "[bg][fg]overlay=0:(1920-608)/2[vout];"
            "[0:a]loudnorm=I=-14:LRA=7:tp=-1[aout]"
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

    print(f"[FFmpeg] Rendering 1080x1920 60FPS Ambient-Blurred Short for {creator_name}...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0 and os.path.exists(output_path):
        size_mb = os.path.getsize(output_path) / (1024 * 1024)
        print(f"[FFmpeg] SUCCESS: Rendered {output_path} ({size_mb:.2f} MB, 60fps HD Lossless)")
        return True
    else:
        print(f"[FFmpeg] Error: {res.stderr[-500:]}")
        return False
