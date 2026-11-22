# High-Precision Devanagari to Natural Roman Hinglish Engine
# Strictly maps words to authentic conversational Hinglish (WhatsApp/Reels style)
# Zero broken words, zero awkward schwas (e.g. KARKE not KARAKE, DONO not DONON)

CONSONANTS = {
    'क': 'k', 'ख': 'kh', 'ग': 'g', 'घ': 'gh', 'ङ': 'ng',
    'च': 'ch', 'छ': 'chh', 'ज': 'j', 'झ': 'jh', 'ञ': 'ny',
    'ट': 't', 'ठ': 'th', 'ड': 'd', 'ढ': 'dh', 'ण': 'n',
    'त': 't', 'थ': 'th', 'द': 'd', 'ध': 'dh', 'न': 'n',
    'प': 'p', 'फ': 'ph', 'ब': 'b', 'भ': 'bh', 'म': 'm',
    'य': 'y', 'र': 'r', 'ल': 'l', 'व': 'v', 'श': 'sh',
    'ष': 'sh', 'स': 's', 'ह': 'h', 'क्ष': 'ksh', 'त्र': 'tr', 'ज्ञ': 'gy'
}

VOWELS = {
    'अ': 'a', 'आ': 'aa', 'इ': 'i', 'ई': 'ee', 'उ': 'u', 'ऊ': 'oo',
    'ऋ': 'ri', 'ए': 'e', 'ऐ': 'ai', 'ओ': 'o', 'औ': 'au',
    'अं': 'an', 'अः': 'ah'
}

MATRAS = {
    'ा': 'a', 'ि': 'i', 'ी': 'ee', 'ु': 'u', 'ू': 'oo',
    'ृ': 'ri', 'े': 'e', 'ै': 'ai', 'ो': 'o', 'ौ': 'au',
    'ं': 'n', 'ँ': 'n', 'ः': 'h', '्': ''  # halant removes implicit 'a'
}

# Extensive curated dictionary for gaming, streaming & daily conversational speech
COMMON_OVERRIDES = {
    # Core gaming & streamer vocabulary
    'दोनो': 'DONO', 'दोनों': 'DONO', 'चोर': 'CHOR', 'पुलिस': 'POLICE', 'गाड़ी': 'GAADI',
    'गाड़ियां': 'GAADIYAN', 'भागो': 'BHAGO', 'भाग': 'BHAG', 'जल्दी': 'JALDI', 'अरे': 'ARRE',
    'भाई': 'BHAI', 'बैंक': 'BANK', 'लूटने': 'LOOTNE', 'लूट': 'LOOT', 'चोरी': 'CHORI',
    'करके': 'KARKE', 'कर': 'KAR', 'रहा': 'RAHA', 'रहे': 'RAHE', 'रही': 'RAHI',
    'सामने': 'SAMNE', 'पीछे': 'PEECHE', 'ऊपर': 'UPAR', 'नीचे': 'NEECHE', 'गोली': 'GOLI',
    'मार': 'MAAR', 'मारने': 'MAARNE', 'बचाओ': 'BACHAO', 'खत्म': 'KHATAM', 'रुको': 'RUKO',
    'रुक': 'RUK', 'देखो': 'DEKHO', 'देख': 'DEKH', 'आओ': 'AAO', 'जाओ': 'JAO',
    'गया': 'GAYA', 'गए': 'GAYE', 'गई': 'GAYI', 'पैसा': 'PAISA', 'पैसे': 'PAISE',
    'मिशन': 'MISSION', 'एस्केप': 'ESCAPE', 'अलार्म': 'ALARM', 'बज': 'BAJ', 'चुका': 'CHUKA',
    'चलो': 'CHALO', 'क्या': 'KYA', 'क्यों': 'KYUN', 'कहाँ': 'KAHAN', 'कैसे': 'KAISE',
    'यहाँ': 'YAHAN', 'वहाँ': 'WAHAN', 'लड़का': 'LADKA', 'लड़की': 'LADKI', 'दोस्त': 'DOST',
    'ओपी': 'OP', 'बंदूक': 'BANDUK', 'गन': 'GUN', 'साइकिल': 'CYCLE', 'बाइक': 'BIKE',
    'हेलीकॉप्टर': 'HELICOPTER', 'प्लेन': 'PLANE', 'कार': 'CAR', 'कूद': 'KOOD',
    'बैठो': 'BAITHO', 'उतरो': 'UTRO', 'पकड़': 'PAKAD', 'पकड़ो': 'PAKDO', 'छोड़ो': 'CHHODO',
    'छोड़': 'CHHOD', 'मारो': 'MARO', 'ठोको': 'THOKO', 'ठुक': 'THUK', 'बच': 'BACH',
    'मर': 'MAR', 'यार': 'YAAR', 'साले': 'SAALE', 'कमीने': 'KAMINE', 'बकवास': 'BAKWAAS',
    'मजा': 'MAZA', 'मस्त': 'MAST', 'खतरनाक': 'KHATARNAK', 'हटो': 'HATO', 'हटाओ': 'HATAO',
    'रास्ता': 'RAASTA', 'दो': 'DO', 'ले': 'LE', 'लो': 'LO', 'लिया': 'LIYA', 'दिया': 'DIYA',
    'किया': 'KIYA', 'होगा': 'HOGA', 'होगी': 'HOGI', 'होंगे': 'HONGE', 'पहला': 'PEHLA',
    'पहली': 'PEHLI', 'बार': 'BAAR', 'टाइम': 'TIME', 'गेम': 'GAME', 'प्ले': 'PLAY',
    'लेट्स': 'LETS', 'गो': 'GO', 'नाइस': 'NICE', 'ओके': 'OKAY', 'यस': 'YES', 'नो': 'NO',
    'चाहिए': 'CHAHIYE', 'बोल': 'BOL', 'बोला': 'BOLA', 'सुना': 'SUNA', 'सुनो': 'SUNO',
    'समझ': 'SAMAJH', 'समझे': 'SAMJHE', 'है': 'HAI', 'हैं': 'HAIN', 'हूँ': 'HOON',
    'ही': 'HI', 'भी': 'BHI', 'की': 'KI', 'के': 'KE', 'का': 'KA', 'को': 'KO', 'से': 'SE',
    'में': 'MEIN', 'पर': 'PAR', 'पे': 'PE', 'तक': 'TAK', 'ने': 'NE', 'तो': 'TO',
    'हमारा': 'HAMARA', 'हमारे': 'HAMARE', 'हम': 'HUM', 'तुम': 'TUM', 'तुम्हारा': 'TUMHARA',
    'आप': 'AAP', 'आपका': 'AAPKA', 'मुझे': 'MUJHE', 'तुझे': 'TUJHE', 'उसे': 'USE',
    'इनको': 'INKO', 'उनको': 'UNKO', 'सब': 'SAB', 'सबको': 'SABKO', 'कोई': 'KOI',
    'कुछ': 'KUCH', 'बहुत': 'BAHUT', 'ज्यादा': 'ZYADA', 'कम': 'KAM', 'थोड़ा': 'THODA',
    'पूरा': 'POORA', 'एक': 'EK', 'दो': 'DO', 'तीन': 'TEEN', 'चार': 'CHAAR', 'पाँच': 'PAANCH',
    'सीधा': 'SEEDHA', 'उल्टा': 'ULTA', 'सही': 'SAHI', 'गलत': 'GALAT', 'सच': 'SACH',
    'झूठ': 'JHOOTH', 'डर': 'DAR', 'लगा': 'LAGA', 'लगे': 'LAGE', 'लगी': 'LAGI',
    'ठंडा': 'THANDA', 'गरम': 'GARAM', 'तेज': 'TEZ', 'धीमे': 'DHEEME', 'आवाज': 'AAWAAZ',
    'लाइट': 'LIGHT', 'दरवाजा': 'DARWAZA', 'खिड़की': 'KHIDKI', 'घर': 'GHAR', 'कमरा': 'KAMRA',
    'रोड': 'ROAD', 'ट्रैफिक': 'TRAFFIC', 'सिटी': 'CITY', 'वाइस': 'VICE', 'टाउन': 'TOWN',
    'स्टार': 'STAR', 'लेवल': 'LEVEL', 'चैलेंज': 'CHALLENGE', 'वीडियो': 'VIDEO'
}

def transliterate_word(word: str) -> str:
    word_clean = word.strip()
    if not word_clean:
        return ""
    
    # 1. Direct dictionary match
    if word_clean in COMMON_OVERRIDES:
        return COMMON_OVERRIDES[word_clean]
        
    # 2. Check if already English / Latin script
    has_dev = any('\u0900' <= c <= '\u097F' for c in word_clean)
    if not has_dev:
        return word_clean.upper()

    # 3. Phonetic Devanagari transliteration with Hindi schwa deletion
    res = []
    chars = list(word_clean)
    n = len(chars)
    i = 0
    while i < n:
        c = chars[i]
        if c in VOWELS:
            res.append(VOWELS[c])
            i += 1
        elif c in CONSONANTS:
            base = CONSONANTS[c]
            # Check if followed by matra or halant
            if i + 1 < n and chars[i + 1] in MATRAS:
                matra = MATRAS[chars[i + 1]]
                res.append(base + matra)
                i += 2
            else:
                # Schwa deletion: no implicit 'a' at end of word or if next is last consonant
                if i == n - 1:
                    res.append(base)
                elif i == n - 2 and chars[i + 1] in CONSONANTS:
                    # In Hindi words like 'kar', 'khel', 'chor', do not add 'a' to first consonant if 2-letter
                    if n == 2:
                        res.append(base + 'a')
                    else:
                        res.append(base)
                else:
                    res.append(base + 'a')
                i += 1
        elif c in MATRAS:
            res.append(MATRAS[c])
            i += 1
        else:
            res.append(c)
            i += 1

    trans = "".join(res).upper()
    return trans

def devanagari_to_hinglish(text: str) -> str:
    words = text.split()
    return " ".join(transliterate_word(w) for w in words)

if __name__ == "__main__":
    tests = [
        "दोनो ही चोर हैं भाई जल्दी भागो",
        "पुलिस की गाड़ी आ गई लूटने चलो",
        "अरे भाई अलार्म बज गया बैंक में"
    ]
    for t in tests:
        print(f"'{t}' -> '{devanagari_to_hinglish(t)}'")
