import subprocess
import os

def convert_to_vertical_short(input_path: str, output_path: str) -> bool:
    """
    Transforms 16:9 widescreen footage into 9:16 (1080x1920) Vertical Short with:
    - Background: Ambient motion-blurred 9:16 gameplay (optimized fast shader)
    - Foreground: Sharp centered gameplay
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    print(f"Reframing {input_path} to 9:16 vertical short...")
    
    filter_complex = (
        "[0:v]scale=270:480:force_original_aspect_ratio=increase,"
        "crop=270:480,boxblur=5:2,scale=1080:1920[bg];"
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
            print(f"✅ Reframed to vertical: {output_path} ({os.path.getsize(output_path)} bytes)")
            return True
    except Exception as e:
        print(f"Error during video reframing: {e}")
        
    return False
