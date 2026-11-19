import random

TECHNO_YT_TITLES = [
    "TECHNO GAMERZ FIRST DAY IN VICE CITY! 🚨🔥 Police Heist Escape #shorts #technogamerz #gta6",
    "TECHNO GAMERZ INSANE 5-STAR POLICE CHASE IN GTA 6! 🏎️💨 #shorts #technogamerz",
    "TECHNO GAMERZ CAN'T BELIEVE THIS GTA 6 DETAIL! 🤯🎮 #shorts #techno",
    "LUCIA & UJJWAL CRAZIEST ESCAPE IN GTA 6! 💀🔥 #shorts #gta6"
]

CARRY_YT_TITLES = [
    "CARRYMINATI CRAZIEST GTA RAMP STUNT! 💀🚗 (BAL BAL BACHE) #shorts #carryislive #gta5",
    "CARRYMINATI VS VICE CITY POLICE! 🚨😂 (HILIOUS REACTION) #shorts #carryminati",
    "WHEN CARRY GETS 5-STAR WANTED IN GTA! 🚓💥 #shorts #carryislive"
]

INSAAN_YT_TITLES = [
    "TRIGGERED INSAAN UNREAL GTA 6 REACTION! 😂🔥 #shorts #liveinsaan #gta6",
    "LIVE INSAAN CANNOT STOP LAUGHING IN GTA 6! 💀🎮 #shorts #triggeredinsaan"
]

def generate_dual_metadata(creator_name: str = "Techno Gamerz") -> dict:
    c_lower = creator_name.lower()

    if "techno" in c_lower or "ujjwalgamer" in c_lower:
        yt_title = random.choice(TECHNO_YT_TITLES)
        yt_desc = (
            "Techno Gamerz gets caught in an insane GTA 6 Vice City police chase! 🚨🎮\n\n"
            "Watch Ujjwal and Lucia pull off the craziest rooftop heist escape! Like & SUBSCRIBE to GTA 6 VICE HUB for daily 60FPS Indian gaming stream moments!\n\n"
            "#shorts #technogamerz #gta6 #gaming #ytshorts #techno #ujjwalgamer #vicecity #gta #viral"
        )
        yt_tags = ["shorts", "technogamerz", "gta6", "gaming", "ytshorts", "techno", "ujjwalgamer", "vicecity", "viral"]

        ig_caption = (
            "TECHNO GAMERZ IN GTA 6! 🚨 Vice City Rooftop Alarm & Police Escape! 🔥\n\n"
            "When the alarm goes off and Vice City cops pull up... Lucia and Ujjwal escape! 💀🎮\n\n"
            "Watch full 60FPS Shorts on YouTube: @gta6vicehubind 🌴\n\n"
            "#gta6 #technogamerz #gaming #reels #gta #vicecity #gta6gameplay #indianstreamer #viralreels #explorepage #indiangaming"
        )
    elif "carry" in c_lower:
        yt_title = random.choice(CARRY_YT_TITLES)
        yt_desc = (
            "CarryisLive attempts the wildest stunts and police chases in GTA! 😂🔥\n\n"
            "Like & SUBSCRIBE to GTA 6 VICE HUB for daily high-energy stream highlights!\n\n"
            "#shorts #carryminati #carryislive #gta5 #gta #gaming #viral #funny #ytshorts"
        )
        yt_tags = ["shorts", "carryminati", "carryislive", "gta5", "gta", "gaming", "viral", "funny", "ytshorts"]

        ig_caption = (
            "CARRYMINATI CRAZIEST GTA ESCAPE! 💀🔥 Bal Bal Bache!\n\n"
            "When CarryisLive takes on the cops in GTA... pure comedy! 😂🎮\n\n"
            "Follow @grow10z for daily Indian gaming clips! 🌴\n\n"
            "#carryminati #carryislive #gta #gta6 #gamingreels #viralreels #indianstreamer #explorepage #indiangaming"
        )
    else:
        yt_title = random.choice(INSAAN_YT_TITLES)
        yt_desc = (
            "Triggered Insaan funniest gaming reaction in GTA! 🎮😂\n\n"
            "Like & SUBSCRIBE to GTA 6 VICE HUB for daily top Indian streamer moments!\n\n"
            "#shorts #liveinsaan #triggeredinsaan #gta6 #gaming #ytshorts #viral"
        )
        yt_tags = ["shorts", "liveinsaan", "triggeredinsaan", "gta6", "gaming", "ytshorts"]

        ig_caption = (
            "TRIGGERED INSAAN WILD GTA REACTION! 😂🔥\n\n"
            "When Live Insaan plays GTA... non-stop entertainment! 💀🎮\n\n"
            "Follow @grow10z for daily viral gaming reels! 🌴\n\n"
            "#liveinsaan #triggeredinsaan #gta6 #gamingreels #viralreels #indianstreamer #explorepage"
        )

    return {
        "yt_title": yt_title,
        "yt_desc": yt_desc,
        "yt_tags": yt_tags,
        "ig_caption": ig_caption
    }
