import re
import os
from src.devanagari_to_hinglish import transliterate_word

def to_sec(ts: str) -> float:
    parts = ts.split(':')
    if len(parts) == 3:
        h = int(parts[0])
        m = int(parts[1])
        s = float(parts[2])
        return h * 3600 + m * 60 + s
    elif len(parts) == 2:
        m = int(parts[0])
        s = float(parts[1])
        return m * 60 + s
    return 0.0

def parse_vtt_words(vtt_path: str, start_sec: float, end_sec: float) -> list:
    """
    Parses word-by-word microsecond tags from YouTube auto-generated VTT (<00:10:51.300><c> शब्द</c>).
    Converts Hindi/Devanagari automatically to Roman Hinglish (ZERO pure Hindi script).
    Returns list of (timestamp_rel, word).
    """
    if not os.path.exists(vtt_path):
        return []

    with open(vtt_path, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()

    raw_events = []
    for line in lines:
        line = line.strip()
        if not line or '-->' in line or line.startswith('WEBVTT') or line.startswith('Kind:') or line.startswith('Language:'):
            continue

        matches = list(re.finditer(r'<(\d{2}:\d{2}:\d{2}\.\d{3})><c>\s*([^<]+)</c>', line))
        for m in matches:
            ts, word = m.groups()
            sec = to_sec(ts)
            # Filter clean words (no emojis)
            clean_w = re.sub(r'[^\w\s\u0900-\u097F!?.,\'-]', '', word).strip()
            if clean_w and start_sec <= sec <= end_sec:
                hinglish_w = transliterate_word(clean_w)
                if hinglish_w:
                    raw_events.append((sec - start_sec, hinglish_w))

    # Deduplicate closely spaced duplicate words
    deduped = []
    for sec, w in raw_events:
        if not deduped or (abs(sec - deduped[-1][0]) > 0.08 or w != deduped[-1][1]):
            deduped.append((sec, w))

    return deduped

def generate_word_by_word_ass(ass_path: str, word_list: list, total_duration: float = 45.0) -> bool:
    """
    Builds broadcast-quality ASS subtitles with:
    - 1-2 words popping dynamically with scale bounce (\fscx125\fscy125).
    - 100% Hinglish in Roman alphabet (NO Devanagari script).
    - Zero emojis on screen.
    - Captions appear ONLY when speaking; zero captions during silence.
    - Lower third placement (MarginV: 240) over gameplay; 100% clean middle split.
    """
    colors = [
        "&H0000FFFF&",  # Bold Yellow
        "&H002BF750&",  # Electric Green
        "&H000000FF&",  # Vibrant Red
        "&H00FFFF00&"   # Neon Cyan
    ]

    ass_header = """[Script Info]
Title: GTA 6 Cloud Autonomous Word By Word Subtitles
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: HeaderTitle,Impact,52,&H00FFFFFF,&H00FFFFFF,&H00000000,&H90000000,-1,0,0,0,100,100,2,0,1,6,3,8,40,40,220,1
Style: PopWord,Impact,78,&H0000FFFF,&H00FFFFFF,&H00000000,&HA0000000,-1,0,0,0,105,105,2,0,1,8,4,2,40,40,340,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.00,0:02:00.00,HeaderTitle,,0,0,0,,TECHNO GAMERZ • GTA 6

"""

    dialogue_lines = []

    if word_list and len(word_list) >= 5:
        # Group into 1-2 words punchy phrases
        i = 0
        color_idx = 0
        while i < len(word_list):
            group_size = 2 if (i % 3 == 0) else 1
            chunk = word_list[i : i + group_size]
            t_start = chunk[0][0]
            # End time is next word's start time or t_start + 1.2s max
            if i + group_size < len(word_list):
                t_end = min(word_list[i + group_size][0], t_start + 1.4)
            else:
                t_end = min(t_start + 1.2, total_duration)

            # Silence guard: If gap to next word is large, end subtitle strictly at spoken duration
            if t_end - t_start > 1.4:
                t_end = t_start + 0.9

            phrase = " ".join(w for _, w in chunk).strip()
            if phrase:
                start_m = int(t_start // 60)
                start_s = t_start % 60
                end_m = int(t_end // 60)
                end_s = t_end % 60

                col = colors[color_idx % len(colors)]
                color_idx += 1

                # Pop animation: scale bounce from 125% to 100%
                effect_text = f"{{\\c{col}\\t(0,80,\\fscx125\\fscy125)\\t(80,160,\\fscx100\\fscy100)}}{phrase}"
                line = f"Dialogue: 0,0:{start_m:02d}:{start_s:05.2f},0:{end_m:02d}:{end_s:05.2f},PopWord,,0,0,0,,{effect_text}\n"
                dialogue_lines.append(line)

            i += group_size
    else:
        # Fallback
        pass

    with open(ass_path, "w", encoding="utf-8") as f:
        f.write(ass_header + "".join(dialogue_lines))

    print(f"[Captions] Created word-by-word Hinglish ASS with {len(dialogue_lines)} speech events (Hinglish Roman script, Zero emojis, Silence VAD).")
    return True
