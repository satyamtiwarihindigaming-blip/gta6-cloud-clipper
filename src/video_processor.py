import subprocess
import os
import random

def generate_viral_captions_ass(ass_path: str, duration: int = 45):
    """
    Generates dynamic, word-by-word bouncing ASS subtitles with neon color highlights.
    Placed strictly in the lower third (MarginV: 240) over the gameplay, leaving the middle clean.
    """
    ass_header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: PopYellow,Impact,74,&H0000FFFF,&H00FFFFFF,&H00000000,&H90000000,-1,0,0,0,105,105,2,0,1,7,4,2,40,40,240,1
Style: PopCyan,Impact,74,&H00FFFF00,&H00FFFFFF,&H00000000,&H90000000,-1,0,0,0,105,105,2,0,1,7,4,2,40,40,240,1
Style: PopGreen,Impact,76,&H002BF750,&H00FFFFFF,&H00000000,&H90000000,-1,0,0,0,110,110,2,0,1,8,4,2,40,40,240,1
Style: PopRed,Impact,78,&H000000FF,&H00FFFFFF,&H00000000,&H90000000,-1,0,0,0,110,110,2,0,1,7,4,2,40,40,240,1
Style: PopWhite,Impact,70,&H00FFFFFF,&H0000FFFF,&H00000000,&H90000000,-1,0,0,0,100,100,2,0,1,6,3,2,40,40,240,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    bursts = [
        ("PopYellow", "{\\fscx115\\fscy115}BRO WAIT! 😱{\\r}"),
        ("PopWhite", "LOOK AT THIS!!"),
        ("PopGreen", "{\\fscx120\\fscy120}IS THIS GTA 6?! 🤯{\\r}"),
        ("PopCyan", "{\\fscx115\\fscy115}VICE CITY BEACH! 🏖️{\\r}"),
        ("PopRed", "OH MY GOD!! 💀"),
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
        ("PopRed", "{\\fscx130\\fscy130}GTA 6 GOTY CONFIRMED! 🏆🔥{\\r}"),
        ("PopYellow", "SUBSCRIBE FOR DAILY CLIPS! 🔔❤️")
    ]
    
    events = []
    t = 0.5
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

def convert_to_vertical_short(input_path: str, output_path: str, creator_name: str = "Streamer") -> bool:
    """
    Transforms footage into high-retention 9:16 Vertical Short with:
    - Top: Streamer Facecam / Action closeup (1080x960)
    - Bottom: Centered Gameplay (1080x960)
    - Middle: CLEAN SPLIT - ZERO text in the middle!
    - Captions: Dynamic Bouncing ASS in Lower Third (MarginV: 240)
    - Loudness normalized audio (-14 LUFS)
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    temp_dir = os.path.dirname(output_path)
    
    ass_path = os.path.join(temp_dir, "cloud_captions.ass")
    generate_viral_captions_ass(ass_path, duration=45)
    
    ass_escaped = ass_path.replace("\\", "/").replace(":", "\\:")

    # Top facecam: 1080x960, Bottom gameplay: 1080x960, Middle clean split (no text)
    filter_complex = (
        "[0:v]crop=in_w*0.45:in_h*0.45:0:in_h*0.35,scale=1080:960:force_original_aspect_ratio=increase,crop=1080:960[top];"
        "[0:v]crop=in_w*0.65:in_h*0.8:in_w*0.35:0,scale=1080:960:force_original_aspect_ratio=increase,crop=1080:960[bot];"
        "[top][bot]vstack[vstacked];"
        f"[vstacked]ass='{ass_escaped}'[v];"
        "[0:a]loudnorm=I=-14:TP=-1.5:LRA=11[a]"
    )
    
    cmd = [
        "ffmpeg", "-y",
        "-i", input_path,
        "-filter_complex", filter_complex,
        "-map", "[v]",
        "-map", "[a]",
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "23",
        "-r", "30",
        "-c:a", "aac",
        "-b:a", "128k",
        "-t", "45",
        output_path
    ]
    
    print(f"Running FFmpeg split-screen render (Clean middle, Lower captions): {' '.join(cmd)}")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"FFmpeg render error: {res.stderr[-500:]}")
        return False
    return True
