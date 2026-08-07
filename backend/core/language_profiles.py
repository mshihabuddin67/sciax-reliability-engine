def detect_language_profile(text):

    languages = []

    text_lower = text.lower()

    bangla_score = 0
    hindi_score = 0
    english_score = 0

    # ----------------------------------
    # Bangla Script
    # ----------------------------------

    if any("\u0980" <= c <= "\u09FF" for c in text):
        languages.append("Bangla")

    # ----------------------------------
    # Hindi Script
    # ----------------------------------

    if any("\u0900" <= c <= "\u097F" for c in text):
        languages.append("Hindi")

    # ----------------------------------
    # Romanized Bangla
    # ----------------------------------

    roman_bangla_markers = [

        "toke",
        "tore",
        "tomake",
        "tomar",
        "tumi",

        "ami",

        "shesh",
        "sesh",
        "mere",
        "felbo",

        "marbo",
        "morbi",
        "khun",

        "dibo",
        "debo",
        "dibe",
        "dibi",

        "korbo",
        "kore",
        "koris",

        "nibo",
        "nebo",

        "dekhis",
        "hobe",
        "hobena",
        "hoy",
        "mon",
        "valo",
        "bhalo",

        "nis",
        "re",
        "pagol",
        "ekdin"
    ]

    for marker in roman_bangla_markers:
        if marker in text_lower:
            bangla_score += 1

    # ----------------------------------
    # Roman Hindi
    # ----------------------------------

    roman_hindi_markers = [

        "tujhe",
        "tumhe",
        "mujhe",

        "mar dunga",
        "maar dunga",
        "dunga",

        "khatam kar dunga",
        "dekh lunga",

        "karunga",
        "nahi",
        "mat"
    ]

    for marker in roman_hindi_markers:
        if marker in text_lower:
            hindi_score += 1

    # ----------------------------------
    # English
    # ----------------------------------

    english_markers = [

        "hack",
        "system",
        "sleep",
        "schedule",

        "force",
        "release",

        "kill",
        "you",
        "will",

        "password",
        "account",
        "credential",

        "otp",
        "support",

        "pretend",
        "impersonate",

        "breach",
        "exploit",

        "harass",
        "bully"
    ]

    for marker in english_markers:
        if marker in text_lower:
            english_score += 1

    # ----------------------------------
    # Score Threshold
    # ----------------------------------

    if bangla_score >= 2:
        languages.append("Romanized Bangla")

    if hindi_score >= 2:
        languages.append("Roman Hindi")

    if english_score >= 2:
        languages.append("English")

    # ----------------------------------
    # Default
    # ----------------------------------

    if not languages:
        languages.append("English")

    return list(dict.fromkeys(languages))
