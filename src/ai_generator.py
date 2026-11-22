import os
import re
import json
import random
import urllib.request

def get_gemini_api_key() -> str:
    """Retrieves Google AI Studio Gemini API key from env or local config."""
    key = os.getenv("GEMINI_API_KEY")
    if key and len(key.strip()) > 20:
        return key.strip()
    try:
        import sys
        sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        import config
        key = getattr(config, "GEMINI_API_KEY", "")
        if key and len(key.strip()) > 20:
            return key.strip()
    except Exception:
        pass
    return ""

def call_gemini_api(prompt: str) -> str:
    """Calls Google AI Studio Gemini REST API (gemini-2.5-flash with gemini-1.5-flash fallback)."""
    api_key = get_gemini_api_key()
    if not api_key:
        print("[AI Generator] Note: GEMINI_API_KEY not configured. Using dynamic algorithmic fallback.")
        return ""

    for model in ["gemini-2.5-flash", "gemini-1.5-flash"]:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.85,
                "maxOutputTokens": 600
            }
        }
        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=20) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                text = data["candidates"][0]["content"]["parts"][0]["text"].strip()
                if text:
                    return text
        except Exception as e:
            print(f"[AI Generator] Gemini model {model} attempt note: {e}")

    return ""

def generate_dual_metadata(
    creator_name: str = "Techno Gamerz",
    video_title: str = "GTA 6 Gameplay",
    start_sec: float = 0.0,
    duration: float = 48.0,
    context_words: list = None
) -> dict:
    """
    Generates 100% dynamic, tailored viral metadata using Google AI Studio (Gemini).
    Ensures every clip gets unique high-CTR titles, descriptions, and hashtags for YouTube Shorts & Instagram Reels.
    """
    start_min = int(start_sec // 60)
    start_s = int(start_sec % 60)
    end_sec = start_sec + duration
    end_min = int(end_sec // 60)
    end_s = int(end_sec % 60)
    
    words_summary = " ".join([w for _, w in context_words[:35]]) if context_words else "High intensity gameplay chase and escape"
    
    prompt = f"""You are an elite viral strategist for YouTube Shorts and Instagram Reels (Indian Gaming Niche).
Analyze this specific gameplay moment:
- Streamer / Creator: {creator_name}
- Source Video: {video_title}
- Timestamp: {start_min:02d}:{start_s:02d} to {end_min:02d}:{end_s:02d} ({duration:.0f}s clip)
- Dialogue / Gameplay Context: {words_summary}

Craft viral, high-CTR metadata tailored specifically to what happens in this clip so it blows up on the algorithm on BOTH platforms.

RULES:
1. YouTube Shorts Title:
   - Max 75-85 characters.
   - High curiosity hook + ALL CAPS punchy words + 2 relevant emojis + ends with #shorts.
   - Never duplicate previous generic titles.
   
2. YouTube Description:
   - 2-3 sentence high-energy summary of this exact moment.
   - Call to action to like & subscribe.
   - 8-10 trending gaming hashtags (#shorts #gta6 #technogamerz etc.).

3. YouTube Tags:
   - Array of 8-10 relevant search tags.

4. Instagram Reels Caption:
   - Line 1: Explosive hook line in ALL CAPS with emojis.
   - Line 2-3: Engaging conversational Hinglish / English breakdown of the scene.
   - Call to follow @grow10z for daily stream moments.
   - 12-15 high-reach explore hashtags (#viralreels #gaming #gta6 #technogamerz #explorepage etc.).

Output ONLY valid JSON without markdown fences:
{{
  "yt_title": "...",
  "yt_desc": "...",
  "yt_tags": ["..."],
  "ig_caption": "..."
}}"""

    ai_raw = call_gemini_api(prompt)
    if ai_raw:
        clean_json = re.sub(r'```json\s*', '', ai_raw)
        clean_json = re.sub(r'```\s*', '', clean_json).strip()
        try:
            parsed = json.loads(clean_json)
            if "yt_title" in parsed and "ig_caption" in parsed:
                print(f"[AI Generator] ✅ Google AI Studio (Gemini) generated dynamic viral metadata!")
                print(f"[AI Generator] YouTube: {parsed['yt_title']}")
                return parsed
        except Exception as e:
            print(f"[AI Generator] JSON parsing fallback: {e}")

    # Dynamic fallback with unique timestamp identifiers
    moment_tag = f"{start_min:02d}:{start_s:02d}"
    c_lower = creator_name.lower()
    if "carry" in c_lower:
        yt_title = f"CARRY CRAZIEST GTA ESCAPE AT {moment_tag}! 💀🔥 (BAL BAL BACHE) #shorts"
        yt_desc = f"CarryisLive attempts the wildest stunts and police chases in GTA! Timestamp: {moment_tag}.\n\nLike & SUBSCRIBE for daily high-energy stream highlights!\n\n#shorts #carryminati #carryislive #gta5 #gta #gaming #viral #ytshorts"
        yt_tags = ["shorts", "carryminati", "carryislive", "gta5", "gta", "gaming", "viral"]
        ig_caption = f"CARRY CRAZIEST ESCAPE AT {moment_tag}! 💀🔥\n\nWhen CarryisLive takes on the cops in GTA... pure comedy! 😂🎮\n\nFollow @grow10z for daily clips!\n\n#carryminati #carryislive #gta #gamingreels #viralreels #explorepage"
    else:
        yt_title = f"{creator_name.upper()} INSANE GTA 6 CHASE AT {moment_tag}! 🏎️💨 #shorts"
        yt_desc = f"{creator_name} gets caught in an insane Vice City chase at {moment_tag}! 🚨🎮\n\nWatch the full 60FPS action! Like & SUBSCRIBE for daily Indian gaming stream moments!\n\n#shorts #technogamerz #gta6 #gaming #ytshorts #vicecity #viral"
        yt_tags = ["shorts", "technogamerz", "gta6", "gaming", "ytshorts", "vicecity", "viral"]
        ig_caption = f"{creator_name.upper()} IN VICE CITY AT {moment_tag}! 🚨 INSANE ESCAPE! 🔥\n\nWhen the alarm goes off and cops pull up... epic escape! 💀🎮\n\nFollow @grow10z for daily stream moments! 🌴\n\n#gta6 #technogamerz #gaming #reels #vicecity #viralreels #explorepage"

    return {
        "yt_title": yt_title,
        "yt_desc": yt_desc,
        "yt_tags": yt_tags,
        "ig_caption": ig_caption
    }
