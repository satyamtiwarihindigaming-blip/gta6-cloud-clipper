import random
import google.generativeai as genai
from .config import GEMINI_API_KEY

FALLBACK_TITLES = [
    "THIS GTA 6 MOMENT BROKE THE INTERNET! 💀🔥 #shorts",
    "HE FOUND THIS SECRET IN GTA 6?! 😱 #shorts",
    "THE CRAZIEST POLICE CHASE IN GTA 6! 🚓💥 #shorts",
    "BRO WAS NOT READY FOR THIS IN GTA 6 😂 #shorts",
    "IS THIS THE BEST GTA 6 EASTER EGG YET? 🤯 #shorts"
]

FALLBACK_TAGS = "#GTA6 #GTA6Gameplay #GamingShorts #GrandTheftAuto6 #Gaming #Shorts #Viral"

def generate_viral_metadata(streamer_name: str = "Streamer") -> tuple[str, str, str]:
    """
    Returns (Title, Description, Tags) using Gemini API or smart viral fallbacks.
    """
    if GEMINI_API_KEY:
        try:
            genai.configure(api_key=GEMINI_API_KEY)
            model = genai.GenerativeModel("gemini-2.5-flash")
            prompt = f"""
            Generate viral social media metadata for a crazy GTA 6 livestream clip from {streamer_name}.
            Keep title under 65 chars with high-CTR emojis.
            
            Return exactly in this format:
            TITLE: <title>
            DESCRIPTION: <short 2-sentence description>
            TAGS: <5-8 hashtags starting with #>
            """
            response = model.generate_content(prompt)
            text = response.text.strip().split("\n")
            
            title = None
            desc = f"Unreal GTA 6 gameplay moment live on stream! Like and subscribe for more GTA 6 clips. #shorts"
            tags = FALLBACK_TAGS
            
            for line in text:
                if line.startswith("TITLE:"):
                    title = line.replace("TITLE:", "").strip()
                elif line.startswith("DESCRIPTION:"):
                    desc = line.replace("DESCRIPTION:", "").strip()
                elif line.startswith("TAGS:"):
                    tags = line.replace("TAGS:", "").strip()
            
            if title:
                return title, desc, tags
        except Exception as e:
            print(f"Gemini API warning (using fallback): {e}")

    # Fallback if no key or error
    title = random.choice(FALLBACK_TITLES)
    desc = f"Watch this insane GTA 6 live stream clip! Subscribe for daily viral moments."
    return title, desc, FALLBACK_TAGS
