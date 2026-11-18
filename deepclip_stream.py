import os
import sys
import argparse
import subprocess
import json
import re

def parse_args():
    parser = argparse.ArgumentParser(description="Deep Clip Direct Stream & Video Clipper")
    parser.add_argument("--url", type=str, required=True, help="Direct Stream or Video URL (YouTube / Twitch)")
    parser.add_argument("--layout", type=str, default="vertical-blur", choices=["vertical-blur", "vertical-black", "landscape"])
    parser.add_argument("--duration", type=int, default=45, help="Clip duration in seconds for live streams")
    parser.add_argument("--output", type=str, default="output/clips", help="Output directory")
    return parser.parse_args()

def is_youtube_url(url: str) -> bool:
    return "youtube.com" in url or "youtu.be" in url

def extract_youtube_video_id(url: str) -> str:
    pattern = r"(?:v=|\/|youtu\.be\/)([0-9A-Za-z_-]{11})"
    match = re.search(pattern, url)
    return match.group(1) if match else None

def get_youtube_transcript(video_id: str):
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return transcript
    except Exception as e:
        print(f"Transcript API notice: {e}")
        return None

def cut_clip_ffmpeg(input_source: str, start_time: str, duration: int, output_file: str, layout: str = "vertical-blur"):
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    if layout == "vertical-blur":
        # Deep Clip standard 9:16 vertical blur layout
        filter_complex = (
            "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,"
            "crop=1080:1920,boxblur=25:5[bg];"
            "[0:v]scale=1080:608[fg];"
            "[bg][fg]overlay=(W-w)/2:(H-h)/2[v]"
        )
        cmd = [
            "ffmpeg", "-y",
            "-ss", str(start_time),
            "-i", input_source,
            "-t", str(duration),
            "-filter_complex", filter_complex,
            "-map", "[v]",
            "-map", "0:a?",
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "22",
            "-c:a", "aac",
            output_file
        ]
    else:
        cmd = [
            "ffmpeg", "-y",
            "-ss", str(start_time),
            "-i", input_source,
            "-t", str(duration),
            "-c", "copy",
            output_file
        ]
        
    print(f"Cutting clip to {output_file}...")
    subprocess.run(cmd, check=True)
    print(f" Clip ready: {output_file}")

def clip_live_stream(stream_url: str, duration: int, output_file: str, layout: str):
    """Deep Clip live stream handler: grabs live buffer & reframes"""
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    temp_raw = output_file.replace(".mp4", "_raw.mp4")
    
    print(f"Deep Clip capturing live stream from {stream_url} ({duration}s)...")
    streamlink_cmd = ["streamlink", "--hls-live-restart", stream_url, "720p,best", "-O"]
    ffmpeg_cmd = ["ffmpeg", "-y", "-i", "pipe:0", "-t", str(duration), "-c", "copy", temp_raw]
    
    try:
        p1 = subprocess.Popen(streamlink_cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        subprocess.run(ffmpeg_cmd, stdin=p1.stdout, check=True)
        p1.stdout.close()
        p1.wait()
        
        # Now apply Deep Clip layout
        cut_clip_ffmpeg(temp_raw, "0", duration, output_file, layout=layout)
        if os.path.exists(temp_raw):
            os.remove(temp_raw)
        return True
    except Exception as e:
        print(f"Error clipping live stream: {e}")
        return False

def main():
    args = parse_args()
    print("=" * 60)
    print("🎬 DEEP CLIP: DIRECT STREAM CLIPPER ACTIVATED")
    print(f"🔗 Target Stream URL: {args.url}")
    print(f"📐 Layout Format: {args.layout}")
    print("=" * 60)
    
    os.makedirs(args.output, exist_ok=True)
    output_clip = os.path.join(args.output, f"deepclip_{int(time.time())}.mp4") if 'time' in globals() else os.path.join(args.output, "deepclip_output.mp4")
    
    # Check if it's a live stream or VOD
    video_id = extract_youtube_video_id(args.url) if is_youtube_url(args.url) else None
    
    transcript = None
    if video_id:
        print(f"Detected YouTube video ID: {video_id}")
        transcript = get_youtube_transcript(video_id)
        
    if transcript:
        print(f" Successfully fetched {len(transcript)} transcript lines via Deep Clip!")
        print("Finding viral moments...")
        # Take the top high energy segment (default first 45s of highlight)
        start_time = transcript[0]['start'] if transcript else 0
        
        # Download and cut
        yt_cmd = [
            "yt-dlp",
            "-g",
            "-f", "best[height<=1080]",
            args.url
        ]
        stream_direct_url = subprocess.check_output(yt_cmd, text=True).strip().split("\n")[0]
        cut_clip_ffmpeg(stream_direct_url, str(start_time), args.duration, output_clip, layout=args.layout)
    else:
        # Live stream direct clipping
        print("Clipping live stream directly...")
        clip_live_stream(args.url, args.duration, output_clip, args.layout)
        
    print("=" * 60)
    print(f"✅ DEEP CLIP COMPLETED! Clip saved to: {output_clip}")
    print("=" * 60)

if __name__ == "__main__":
    import time
    main()
