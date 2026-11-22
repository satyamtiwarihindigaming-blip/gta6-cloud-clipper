import os
import sys
import time
from src.live_monitor import find_target_video, download_subtitles_and_find_viral_moment, load_history, save_history
from src.stream_recorder import record_slice_segment
from src.video_processor import convert_to_vertical_short
from src.ai_generator import generate_dual_metadata
from src.uploader import upload_to_socials

def run():
    print("=" * 60)
    print("🚀 24/7 AUTONOMOUS GTA 6 & TECHNO GAMERZ CLOUD CLIPPER")
    print("   Running in Cloud | 1080p60 Zero Blur | Word-by-Word VAD")
    print("=" * 60)

    output_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(output_dir, exist_ok=True)
    temp_dir = os.path.join(os.path.dirname(__file__), "temp_downloads")
    os.makedirs(temp_dir, exist_ok=True)

    timestamp = int(time.time())
    raw_slice = os.path.join(temp_dir, f"raw_slice_{timestamp}.mp4")
    final_short = os.path.join(output_dir, f"short_{timestamp}.mp4")

    # Step 1: Find target streamer / video (Techno Gamerz GTA 6 priority)
    video_id, video_url, creator_name = find_target_video()
    print(f"\n[Step 1] Target Selected: {creator_name} ({video_id})")

    # Step 2: Download subtitles and find viral speech moment (45-50s)
    print("\n[Step 2] Scanning speech density and detecting best viral moment...")
    start_sec, end_sec, vtt_file, word_list = download_subtitles_and_find_viral_moment(video_id, temp_dir)
    duration = end_sec - start_sec
    print(f"Selected Moment: {start_sec:.1f}s to {end_sec:.1f}s ({duration:.1f}s, {len(word_list)} words)")

    # Step 3: Download 1080p slice
    print("\n[Step 3] Downloading 1080p stream slice...")
    downloaded = record_slice_segment(video_url, raw_slice, start_sec=start_sec, duration=duration)
    if not downloaded or not os.path.exists(raw_slice):
        print("❌ Could not download video segment. Exiting.")
        sys.exit(1)

    # Step 4: Vertical Reframing (Facecam Top + Gameplay Bottom + Word-by-Word Captions)
    print("\n[Step 4] Rendering 9:16 Vertical Short (1080x1920 60FPS)...")
    rendered = convert_to_vertical_short(
        input_path=raw_slice,
        output_path=final_short,
        creator_name=creator_name,
        word_list=word_list,
        duration=duration
    )
    if not rendered or not os.path.exists(final_short):
        print("❌ Video rendering failed. Exiting.")
        sys.exit(1)

    # Step 5: Generate Dual Platform Metadata with Google AI Studio (Gemini)
    print("\n[Step 5] Generating Dynamic Viral Metadata with Google AI Studio (Gemini)...")
    metadata = generate_dual_metadata(
        creator_name=creator_name,
        video_title=f"{creator_name} GTA Gameplay ({video_id})",
        start_sec=start_sec,
        duration=duration,
        context_words=word_list
    )
    print(f"YouTube Title: {metadata['yt_title']}")
    print(f"Instagram Caption:\n{metadata['ig_caption']}")

    # Step 6: Publish to YouTube Shorts and Instagram Reels (Buffer)
    print("\n[Step 6] Publishing to Platforms...")
    results = upload_to_socials(final_short, metadata)
    print(f"Upload Results: {results}")

    # Step 7: Record into history.json
    history = load_history()
    history.setdefault("processed_moments", []).append(start_sec)
    history.setdefault("posted_clips", []).append({
        "video_id": video_id,
        "creator": creator_name,
        "start_sec": start_sec,
        "duration": duration,
        "timestamp": timestamp,
        "youtube": results.get("youtube_url"),
        "instagram": results.get("instagram_success")
    })
    save_history(history)
    print("\n[Step 7] History updated in history.json.")

    # Cleanup raw slice to save space
    if os.path.exists(raw_slice):
        try:
            os.remove(raw_slice)
        except Exception:
            pass

    print("\n" + "=" * 60)
    print("🎉 RUN COMPLETE! VIDEO PUBLISHED TO YOUTUBE & INSTAGRAM!")
    print("=" * 60)

if __name__ == "__main__":
    run()
