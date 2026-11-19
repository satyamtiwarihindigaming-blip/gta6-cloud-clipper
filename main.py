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
    print("🚀 GTA 6 & TOP STREAMERS AUTONOMOUS CLOUD CLIPPER")
    print("==================================================")
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    timestamp = int(time.time())
    raw_video = os.path.join(OUTPUT_DIR, f"raw_{timestamp}.mp4")
    vertical_video = os.path.join(OUTPUT_DIR, f"short_{timestamp}.mp4")
    
    # Step 1: Detect live streamer (Mythpat, Carry, Speed) or GTA 6 trending video
    active_url, creator_name = find_active_streamer(TARGET_STREAMERS)
    print(f"🎬 Target Content Selected: {creator_name} ({active_url})")
    
    # Step 2: Record/Extract 45s Segment
    recorded = record_live_segment(active_url, raw_video, duration=CLIP_DURATION)
    if not recorded:
        print("❌ Could not extract video segment.")
        sys.exit(1)
        
    # Step 3: Reframing 16:9 -> 9:16 Vertical Short
    reframed = convert_to_vertical_short(raw_video, vertical_video)
    if not reframed:
        print("❌ Reframing failed.")
        sys.exit(1)
        
    # Step 4: Generate Viral Title, Description & Hashtags
    title, desc, tags = generate_viral_metadata(creator_name)
    print(f"📝 Title: {title}")
    print(f"📄 Description:\n{desc}")
    print(f"🏷️ Tags: {tags}")
    
    # Step 5: Post directly to YouTube as PUBLIC Short
    upload_to_socials(vertical_video, title, desc, tags)
    
    # Step 6: Ping Phone via Telegram
    notify_user(title, tags, vertical_video)
    
    # Clean up raw file to save disk space
    if os.path.exists(raw_video):
        os.remove(raw_video)
        
    print("==================================================")
    print("🎉 RUN COMPLETED! SHORT PUBLISHED TO YOUTUBE!")
    print("==================================================")

if __name__ == "__main__":
    run()
