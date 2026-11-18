import os
import sys
import time
from src.config import TARGET_STREAMERS, CLIP_DURATION, OUTPUT_DIR
from src.live_monitor import find_active_streamer
from src.stream_recorder import record_live_segment
from src.video_processor import convert_to_vertical_short
from src.ai_generator import generate_viral_metadata
from src.telegram_notifier import notify_user
from src.uploader import upload_to_socials

def run():
    print("==================================================")
    print("🚀 GTA 6 CLOUD CLIPPER: AUTONOMOUS RUN STARTED")
    print("==================================================")
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    timestamp = int(time.time())
    raw_video = os.path.join(OUTPUT_DIR, f"raw_{timestamp}.mp4")
    vertical_video = os.path.join(OUTPUT_DIR, f"short_{timestamp}.mp4")
    
    # Step 1: Detect live streamer
    active_streamer = find_active_streamer(TARGET_STREAMERS)
    if not active_streamer:
        print("ℹ️ No target streamers currently live. Exiting run peacefully.")
        sys.exit(0)
        
    streamer_name = active_streamer.rstrip("/").split("/")[-1]
    print(f"🎬 Active Streamer: {streamer_name}")
    
    # Step 2: Record Live Buffer
    recorded = record_live_segment(active_streamer, raw_video, duration=CLIP_DURATION)
    if not recorded:
        print("❌ Could not record segment from stream.")
        sys.exit(1)
        
    # Step 3: Reframing 16:9 -> 9:16 Vertical Short
    reframed = convert_to_vertical_short(raw_video, vertical_video)
    if not reframed:
        print("❌ Reframing failed.")
        sys.exit(1)
        
    # Step 4: Generate Viral Title & Tags
    title, desc, tags = generate_viral_metadata(streamer_name)
    print(f"📝 Title: {title}")
    print(f"🏷️ Tags: {tags}")
    
    # Step 5: Post to Socials / Webhooks
    upload_to_socials(vertical_video, title, desc, tags)
    
    # Step 6: Ping Phone via Telegram
    notify_user(title, tags, vertical_video)
    
    # Clean up raw horizontal file to save cloud runner disk space
    if os.path.exists(raw_video):
        os.remove(raw_video)
        
    print("==================================================")
    print("✅ RUN COMPLETED SUCCESSFULLY! PC IS CHILLING.")
    print("==================================================")

if __name__ == "__main__":
    run()
