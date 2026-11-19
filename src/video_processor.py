import subprocess
import os
import random
from PIL import Image, ImageDraw, ImageFont

def generate_viral_captions_ass(ass_path: str, duration: int = 45):
    """
    Generates dynamic, word-by-word bouncing ASS subtitles with neon color highlights.
    """
    ass_header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: PopYellow,Impact,74,&H0000FFFF,&H00FFFFFF,&H00000000,&H90000000,-1,0,0,0,105,105,2,0,1,7,4,2,40,40,940,1
Style: PopCyan,Impact,74,&H00FFFF00,&H00FFFFFF,&H00000000,&H90000000,-1,0,0,0,105,105,2,0,1,7,4,2,40,40,940,1
Style: PopGreen,Impact,76,&H002BF750,&H00FFFFFF,&H00000000,&H90000000,-1,0,0,0,110,110,2,0,1,8,4,2,40,40,940,1
Style: PopWhite,Impact,70,&H00FFFFFF,&H0000FFFF,&H00000000,&H90000000,-1,0,0,0,100,100,2,0,1,6,3,2,40,40,940,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    bursts = [
        ("PopYellow", "{\\fscx115\\fscy115}BRO WAIT! 😱{\\r}"),
        ("PopWhite", "LOOK AT THIS!!"),
        ("PopGreen", "{\\fscx120\\fscy120}IS THIS GTA 6?! 🤯{\\r}"),
        ("PopCyan", "{\\fscx115\\fscy115}VICE CITY BEACH! 🏖️{\\r}"),
        ("PopYellow", "OH MY GOD!! 💀"),
        ("PopGreen", "{\\fscx120\\fscy120}THE GRAPHICS ARE UNREAL! 🔥{\\r}"),
        ("PopCyan", "ROCKSTAR COOKED!! 👨‍🍳"),
        ("PopYellow", "{\\fscx125\\fscy125}NO WAY NO WAY! 😂{\\r}"),
        ("PopWhite", "LOOK AT THAT CAR! 🏎️"),
        ("PopGreen", "{\\fscx120\\fscy120}POLICE CHASE STARTED! 🚨{\\r}"),
        ("PopYellow", "5-STAR WANTED LEVEL! 💥"),
        ("PopCyan", "{\\fscx115\\fscy115}RUN RUN RUN! 🏃💨{\\r}"),
        ("PopWhite", "HE HIT A COP CAR! 🚓"),
        ("PopGreen", "{\\fscx125\\fscy125}UNREAL CAR PHYSICS! 💀{\\r}"),
        ("PopYellow", "HE IS TRAPPED! 🚔😂"),
        ("PopCyan", "{\\fscx120\\fscy120}THE NEXT-GEN DETAILS! ✨{\\r}"),
        ("PopGreen", "{\\fscx130\\fscy130}GTA 6 GOTY CONFIRMED! 🏆🔥{\\r}"),
        ("PopYellow", "SUBSCRIBE FOR DAILY CLIPS! 🔔❤️")
    ]
    
    events = []
    t = 0.2
    for style, text in bursts:
        if t >= duration - 1:
            break
        dt = 1.6
        start_str = f"0:{int(t//60):02d}:{t%60:05.2f}"
        end_str = f"0:{int((t+dt)//60):02d}:{(t+dt)%60:05.2f}"
        events.append(f"Dialogue: 0,{start_str},{end_str},{style},,0,0,0,,{text}\n")
        t += dt + 0.1
        
    with open(ass_path, "w", encoding="utf-8") as f:
        f.write(ass_header + "".join(events))

def create_divider_badge(output_png: str, title: str = "GTA 6 VICE HUB"):
    img = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Middle divider box (y=880 to y=1000)
    draw.rectangle([0, 880, 1080, 1000], fill=(10, 8, 22, 255))
    draw.rectangle([0, 874, 1080, 880], fill=(255, 0, 128, 255))   # Neon Magenta Top
    draw.rectangle([0, 1000, 1080, 1006], fill=(0, 240, 255, 255))  # Cyan Bottom

    font = None
    for f in ["C:/Windows/Fonts/impact.ttf", "C:/Windows/Fonts/arialbd.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]:
        if os.path.exists(f):
            try:
                font = ImageFont.truetype(f, 48)
                break
            except Exception:
                pass
    if not font:
        font = ImageFont.load_default()

    badge_text = f"🔥 {title.upper()} 🔥"
    bbox = draw.textbbox((0, 0), badge_text, font=font)
    tw = bbox[2] - bbox[0]
    draw.text(((1080 - tw) / 2 + 2, 912), badge_text, font=font, fill=(0, 0, 0, 255))
    draw.text(((1080 - tw) / 2, 910), badge_text, font=font, fill=(255, 255, 255, 255))

    img.save(output_png, "PNG")

def convert_to_vertical_short(input_path: str, output_path: str, creator_name: str = "Streamer") -> bool:
    """
    Transforms footage into high-retention 9:16 Vertical Short with:
    - Top: Streamer Facecam / Action closeup (1080x880)
    - Bottom: Centered Gameplay (1080x920)
    - Middle: Glowing Neon Cyber Divider Bar
    - Dynamic Bouncing Word-By-Word ASS Captions
    - Loudness normalized audio (-14 LUFS)
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    temp_dir = os.path.dirname(output_path)
    
    divider_png = os.path.join(temp_dir, "cloud_divider.png")
    ass_path = os.path.join(temp_dir, "cloud_captions.ass")
    
    create_divider_badge(divider_png, title=f"{creator_name} x GTA 6")
    generate_viral_captions_ass(ass_path, duration=45)
    
    ass_escaped = ass_path.replace("\\", "/").replace(":", "\\:")

    filter_complex = (
        "[0:v]crop=480:380:800:340,scale=1080:880:force_original_aspect_ratio=increase,crop=1080:880[cam];"
        "[0:v]crop=840:720:0:0,scale=1080:920:force_original_aspect_ratio=increase,crop=1080:920[game];"
        "color=c=black:s=1080x1920:d=45[canvas];"
        "[canvas][cam]overlay=0:0[v1];"
        "[v1][game]overlay=0:1000[v2];"
        f"[v2][1:v]overlay=0:0,ass='{ass_escaped}'[v];"
        "[0:a]loudnorm=I=-14:TP=-1.5:LRA=11[a]"
    )
    
    cmd = [
        "ffmpeg", "-y",
        "-i", input_path,
        "-i", divider_png,
        "-filter_complex", filter_complex,
        "-map", "[v]",
        "-map", "[a]",
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "22",
        "-c:a", "aac",
        "-b:a", "192k",
        output_path
    ]
    
    try:
        subprocess.run(cmd, check=True, timeout=180)
        if os.path.exists(output_path) and os.path.getsize(output_path) > 100000:
            print(f"✅ Masterpiece split-screen rendered: {output_path} ({os.path.getsize(output_path)} bytes)")
            return True
    except Exception as e:
        print(f"Split-screen render attempt error: {e}, falling back to dynamic blur...")
        # Fallback to blurred layout with captions
        fb_filter = (
            "[0:v]scale=270:480:force_original_aspect_ratio=increase,crop=270:480,boxblur=5:2,scale=1080:1920[bg];"
            "[0:v]scale=1080:608[fg];"
            f"[bg][fg]overlay=(W-w)/2:(H-h)/2,ass='{ass_escaped}'[v];"
            "[0:a]loudnorm=I=-14:TP=-1.5:LRA=11[a]"
        )
        fb_cmd = [
            "ffmpeg", "-y",
            "-i", input_path,
            "-filter_complex", fb_filter,
            "-map", "[v]",
            "-map", "[a]",
            "-c:v", "libx264",
            "-preset", "veryfast",
            "-crf", "22",
            "-c:a", "aac",
            output_path
        ]
        try:
            subprocess.run(fb_cmd, check=True, timeout=180)
            return True
        except Exception as e2:
            print(f"Fallback render error: {e2}")
        
    return False
