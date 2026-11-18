import os
from dotenv import load_dotenv

load_dotenv()

# Streamers to monitor (Twitch usernames or YouTube channels)
# Can be overridden via TARGET_STREAMERS env variable (comma-separated)
DEFAULT_STREAMERS = [
    "https://www.twitch.tv/kaicenat",
    "https://www.twitch.tv/xqc",
    "https://www.twitch.tv/shroud",
    "https://www.twitch.tv/jynxzi"
]

TARGET_STREAMERS = [
    s.strip() for s in os.getenv("TARGET_STREAMERS", "").split(",") if s.strip()
] or DEFAULT_STREAMERS

# Video Settings
CLIP_DURATION = int(os.getenv("CLIP_DURATION", "45"))  # Seconds
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "output")

# Cloud API Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL", "")

# YouTube Upload Credentials
YOUTUBE_CLIENT_SECRET = os.getenv("YOUTUBE_CLIENT_SECRET", "")
YOUTUBE_REFRESH_TOKEN = os.getenv("YOUTUBE_REFRESH_TOKEN", "")
