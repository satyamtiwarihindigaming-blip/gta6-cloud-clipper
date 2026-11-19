import os
from dotenv import load_dotenv

load_dotenv()

# Streamers to monitor (YouTube Live channels & Twitch)
DEFAULT_STREAMERS = [
    "https://www.youtube.com/@mythpat/live",
    "https://www.youtube.com/@CarryisLive/live",
    "https://www.youtube.com/@IShowSpeed/live",
    "https://www.twitch.tv/kaicenat",
    "https://www.twitch.tv/xqc"
]

TARGET_STREAMERS = [
    s.strip() for s in os.getenv("TARGET_STREAMERS", "").split(",") if s.strip()
] or DEFAULT_STREAMERS

GTA6_SEARCH_QUERIES = [
    "gta 6 gameplay viral moments",
    "gta 6 insane police chase",
    "mythpat gta 6 funny gameplay",
    "carryislive gta 6 live stream",
    "ishowspeed gta 6 rage moments",
    "gta 6 ultra realistic graphics 4k"
]

# Video Settings
CLIP_DURATION = int(os.getenv("CLIP_DURATION", "45"))  # Seconds
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "output")

# Cloud API Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL", "")
SOCIAL_WEBHOOK_URL = os.getenv("SOCIAL_WEBHOOK_URL", "")

# YouTube Upload Credentials
YOUTUBE_CLIENT_SECRET = os.getenv("YOUTUBE_CLIENT_SECRET", "")
YOUTUBE_REFRESH_TOKEN = os.getenv("YOUTUBE_REFRESH_TOKEN", "")
