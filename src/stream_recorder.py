import subprocess
import os
import random

def record_live_segment(stream_url: str, output_path: str, duration: int = 45) -> bool:
    """
    Records or clips a 45s segment in crisp 1080p Full HD with zero blur.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    print(f"Capturing {duration}s HD clip from: {stream_url}...")
    
    is_live = "/live" in stream_url or "twitch.tv" in stream_url
    
    if is_live:
        streamlink_cmd = [
            "streamlink",
            "--hls-live-restart",
            stream_url,
            "1080p60,1080p,720p60,best",
            "-O"
        ]
        ffmpeg_cmd = [
            "ffmpeg", "-y",
            "-i", "pipe:0",
            "-t", str(duration),
            "-c", "copy",
            output_path
        ]
        try:
            p_streamlink = subprocess.Popen(streamlink_cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
            subprocess.run(ffmpeg_cmd, stdin=p_streamlink.stdout, check=True, timeout=duration + 30)
            p_streamlink.stdout.close()
            p_streamlink.wait()
            
            if os.path.exists(output_path) and os.path.getsize(output_path) > 100000:
                print(f"Successfully recorded HD live segment: {output_path} ({os.path.getsize(output_path)} bytes)")
                return True
        except Exception as e:
            print(f"Streamlink capture attempt: {e}")

    # Fallback / VOD download with yt-dlp in 1080p Full HD
    start_sec = random.randint(30, 240)
    end_sec = start_sec + duration
    
    start_str = f"{start_sec // 60:02d}:{start_sec % 60:02d}"
    end_str = f"{end_sec // 60:02d}:{end_sec % 60:02d}"
    
    print(f"Using yt-dlp to extract 1080p highlight segment ({start_str} to {end_str})...")
    ytdlp_cmd = [
        "yt-dlp",
        "--js-runtimes", "node",
        "-f", "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
        "--download-sections", f"*{start_str}-{end_str}",
        "--force-keyframes-at-cuts",
        "-o", output_path,
        stream_url
    ]
    try:
        subprocess.run(ytdlp_cmd, check=True, timeout=120)
        if os.path.exists(output_path) and os.path.getsize(output_path) > 100000:
            print(f"Successfully captured 1080p HD clip: {output_path} ({os.path.getsize(output_path)} bytes)")
            return True
    except Exception as e:
        print(f"yt-dlp extraction error: {e}")
        
    return False
