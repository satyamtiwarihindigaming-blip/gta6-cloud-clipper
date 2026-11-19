# Devanagari to Roman Hinglish Transliteration Engine

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

# Common gaming & slang vocabulary overrides
COMMON_OVERRIDES = {
    'यह': 'YEH', 'है': 'HAI', 'हमारा': 'HAMARA', 'भाई': 'BHAI', 'पुलिस': 'POLICE',
    'गाड़ी': 'GAADI', 'चलो': 'CHALO', 'भागो': 'BHAGO', 'देखो': 'DEKHO', 'रुको': 'RUKO',
    'अलार्म': 'ALARM', 'बज': 'BAJ', 'गया': 'GAYA', 'चुका': 'CHUKA', 'सामने': 'SAMNE',
    'पीछे': 'PEECHE', 'ऊपर': 'UPAR', 'नीचे': 'NEECHE', 'जल्दी': 'JALDI', 'अरे': 'ARE',
    'क्या': 'KYA', 'क्यों': 'KYUN', 'कहाँ': 'KAHAN', 'कैसे': 'KAISE', 'यहाँ': 'YAHAN',
    'वहाँ': 'WAHAN', 'मारो': 'MARO', 'बचाओ': 'BACHAO', 'खत्म': 'KHATAM', 'ओपी': 'OP',
    'लड़कियां': 'LADKIYAN', 'लड़का': 'LADKA', 'दोस्त': 'DOST', 'मिशन': 'MISSION'
}

def transliterate_word(word: str) -> str:
    word_clean = word.strip()
    if not word_clean:
        return ""
    
    # Check overrides
    if word_clean in COMMON_OVERRIDES:
        return COMMON_OVERRIDES[word_clean]
        
    # Check if contains Devanagari
    has_dev = any('\u0900' <= c <= '\u097F' for c in word_clean)
    if not has_dev:
        return word_clean.upper()

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
                # Implicit 'a' unless end of word or followed by non-devanagari
                if i == n - 1:
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
    test_cases = [
        "यह है हमारा पुलिस",
        "भाई जल्दी भागो अलार्म बज गया",
        "सामने से गाड़ी आ रही है"
    ]
    for tc in test_cases:
        print(f"{tc} -> {devanagari_to_hinglish(tc)}")
