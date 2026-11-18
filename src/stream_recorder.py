import subprocess
import os

def record_live_segment(stream_url: str, output_path: str, duration: int = 45) -> bool:
    """
    Pipes live stream directly from streamlink into ffmpeg to capture exact segment duration.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    print(f"Recording {duration}s live segment from {stream_url}...")
    streamlink_cmd = [
        "streamlink",
        "--hls-live-restart",
        stream_url,
        "720p,best",
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
            print(f" Successfully recorded {output_path} ({os.path.getsize(output_path)} bytes)")
            return True
    except Exception as e:
        print(f"Failed to record live segment: {e}")
        
    return False
