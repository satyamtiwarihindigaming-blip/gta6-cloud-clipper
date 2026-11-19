import random
import os

CREATOR_TAGS = {
    "mythpat": "#mythpat #mythpatlive #gta6 #gaming #shorts #viral #funny",
    "carryislive": "#carryislive #carryminati #gta6 #gaming #shorts #viral #funny",
    "ishowspeed": "#ishowspeed #speed #speedlive #gta6 #gaming #shorts #viral #crazy",
    "kaicenat": "#kaicenat #kai #amp #gta6 #gaming #shorts #viral",
    "xqc": "#xqc #xqclive #gta6 #gaming #shorts #viral"
}

GENERIC_GTA6_TITLES = [
    "THIS GTA 6 MOMENT IS ABSOLUTELY INSANE! 💀🔥 #shorts",
    "BRO WAS NOT READY FOR THIS IN GTA 6 😂🚓 #shorts",
    "THE REALISM IN GTA 6 LOOKS UNREAL! 🤯🏎️ #shorts",
    "5-STAR WANTED IN GTA 6 VICE CITY! 🚨💥 #shorts",
    "CRAZIEST POLICE CHASE IN GTA 6 YET! 🏎️💨 #shorts",
    "WHEN SPEED PLAYS GTA 6 BE LIKE... 💀😂 #shorts"
]

def generate_viral_metadata(streamer_name: str = "Streamer") -> tuple[str, str, str]:
    """
    Returns (Title, Description, Tags) tailored to the creator and GTA 6.
    """
    clean_name = streamer_name.lower().replace("@", "").strip()
    
    # Custom Creator Matching
    if "mythpat" in clean_name:
        title = random.choice([
            "Mythpat's Craziest GTA 6 Moment LIVE! 😂🔥 #shorts",
            "Mythpat Was NOT Ready For This in GTA 6! 💀 #shorts",
            "Mythpat 5-Star Police Chase in Vice City! 🚓😂 #shorts"
        ])
        tags = CREATOR_TAGS["mythpat"]
        desc = (
            f"Mythpat funny moments and crazy gameplay in GTA 6 Vice City! 🎮🔥\n\n"
            f"🔔 Subscribe to GTA 6 VICE HUB for daily viral clips, stream highlights & GTA 6 edits!\n\n"
            f"{tags} #gta6gameplay #ytshorts"
        )
    elif "carry" in clean_name:
        title = random.choice([
            "CarryMinati's Wildest Reaction in GTA 6! 💀🔥 #shorts",
            "CarryisLive GTA 6 Moments You Missed! 😂🎮 #shorts",
            "CarryMinati Police Chase in GTA 6 Vice City! 🚓💥 #shorts"
        ])
        tags = CREATOR_TAGS["carryislive"]
        desc = (
            f"CarryisLive hilarious gameplay and wild reactions in GTA 6! 💥😂\n\n"
            f"🔔 Subscribe to GTA 6 VICE HUB for daily top gaming moments!\n\n"
            f"{tags} #gta6gameplay #ytshorts"
        )
    elif "speed" in clean_name:
        title = random.choice([
            "IShowSpeed's Craziest Rage in GTA 6! 💀⚡ #shorts",
            "Speed Found THIS in GTA 6 Vice City?! 😱🔥 #shorts",
            "When Speed Plays GTA 6 With 5 Stars! 🚨😂 #shorts"
        ])
        tags = CREATOR_TAGS["ishowspeed"]
        desc = (
            f"IShowSpeed wild and funny GTA 6 moments live on stream! 🏎️💨\n\n"
            f"🔔 Subscribe to GTA 6 VICE HUB for daily viral gaming shorts!\n\n"
            f"{tags} #gta6gameplay #ytshorts"
        )
    else:
        title = random.choice(GENERIC_GTA6_TITLES)
        tags = "#GTA6 #GTA6Gameplay #GTA6ViceCity #Gaming #Shorts #Viral #GamingShorts"
        desc = (
            f"Mindblowing GTA 6 next-gen physics and police chase moments in Vice City! 🤯🏎️💨\n\n"
            f"🔔 Subscribe to GTA 6 VICE HUB for daily GTA 6 leaks, viral clips & easter eggs!\n\n"
            f"{tags} #ytshorts"
        )

    return title, desc, tags
