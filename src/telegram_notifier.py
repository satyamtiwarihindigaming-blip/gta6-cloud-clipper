import os
import requests
from .config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, DISCORD_WEBHOOK_URL

def notify_user(title: str, tags: str, video_path: str = None):
    """
    Sends notification to Telegram and/or Discord.
    """
    message = (
        f"🔥 *NEW GTA 6 SHORT GENERATED!* 🔥\n\n"
        f"*Title:* {title}\n"
        f"*Tags:* `{tags}`\n\n"
        f"⚡ *Status:* 100% Cloud Automated. Your PC is OFF & Chilling!"
    )
    
    # 1. Telegram
    if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
        try:
            tg_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
            requests.post(tg_url, json={
                "chat_id": TELEGRAM_CHAT_ID,
                "text": message,
                "parse_mode": "Markdown"
            }, timeout=10)
            print("Telegram alert sent to phone!")
            
            # Send video file if under 50MB
            if video_path and os.path.exists(video_path) and os.path.getsize(video_path) < 45 * 1024 * 1024:
                tg_video_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendVideo"
                with open(video_path, "rb") as f:
                    requests.post(tg_video_url, data={"chat_id": TELEGRAM_CHAT_ID, "caption": title}, files={"video": f}, timeout=60)
                print("Video preview delivered to Telegram!")
        except Exception as e:
            print(f"Telegram notification error: {e}")
            
    # 2. Discord Webhook
    if DISCORD_WEBHOOK_URL:
        try:
            requests.post(DISCORD_WEBHOOK_URL, json={"content": message}, timeout=10)
            print("Discord alert sent!")
        except Exception as e:
            print(f"Discord webhook error: {e}")
