def classify_intent(text):

    text = text.lower().strip()

    intents = []

    # --------------------------------------------------
    # VIOLENT PATTERNS (MULTILINGUAL)
    # --------------------------------------------------

    violent_patterns = [

        # English
        "kill you",
        "murder",
        "destroy you",

        # Banglish
        "mere felbo",
        "khun korbo",
        "shesh kore dibo",
        "shesh kore debo",
        "toke dekhe nibo",
        "ami toke marbo",
        "ami tomake mere felbo",

        # Bangla
        "শেষ করে দিব",
        "শেষ করে দেব",
        "আমি তোকে মারবো",
        "আমি তোমাকে শেষ করে দিব",
        "খুন করবো",
        "মেরে ফেলবো",

        # Hindi
        "mar dunga",
        "tujhe maar dunga",
        "tujhe khatam kar dunga"
    ]

    # --------------------------------------------------
    # CYBER PATTERNS
    # --------------------------------------------------

    cyber_patterns = [

        "hack the system",
        "breach server",
        "bypass security",
        "steal data",
        "exploit vulnerability",

        "system hack korbo",
        "data churi korbo"
    ]

    # --------------------------------------------------
    # SAFE / NON-MALICIOUS CONTEXT
    # --------------------------------------------------

    safe_patterns = [

        "sleep schedule",
        "study hack",
        "life hack",
        "productivity hack",
        "game strategy"
    ]

    # --------------------------------------------------
    # INTENT DETECTION
    # --------------------------------------------------

    for pattern in violent_patterns:
        if pattern in text:
            intents.append("violent_threat")

    for pattern in cyber_patterns:
        if pattern in text:
            intents.append("cyber_intrusion")

    for pattern in safe_patterns:
        if pattern in text:
            intents.append("non-malicious")

    # --------------------------------------------------
    # DEFAULT
    # --------------------------------------------------

    if not intents:
        intents.append("unknown_or_safe")

    return intents
