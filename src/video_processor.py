import subprocess
import os

def convert_to_vertical_short(input_path: str, output_path: str) -> bool:
    """
    Transforms 16:9 widescreen footage into 9:16 (1080x1920) Vertical Short with:
    - Background: Stretched & heavily blurred 9:16 gameplay
    - Foreground: Sharp centered gameplay
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    print(f"Reframing {input_path} to 9:16 vertical short...")
    
    # FFmpeg filter:
    # 1. Scale background to 1080x1920 with boxblur
    # 2. Scale foreground to width 1080
    # 3. Center overlay
    filter_complex = (
        "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,"
        "crop=1080:1920,boxblur=25:5[bg];"
        "[0:v]scale=1080:608[fg];"
        "[bg][fg]overlay=(W-w)/2:(H-h)/2[v]"
    )
    
    cmd = [
        "ffmpeg", "-y",
        "-i", input_path,
        "-filter_complex", filter_complex,
        "-map", "[v]",
        "-map", "0:a?",
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "22",
        "-c:a", "aac",
        "-b:a", "128k",
        output_path
    ]
    
    try:
        subprocess.run(cmd, check=True, timeout=120)
        if os.path.exists(output_path) and os.path.getsize(output_path) > 100000:
            print(f" Reframed to vertical: {output_path}")
            return True
    except Exception as e:
        print(f"Error during video reframing: {e}")
        
    return False
