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
    # SOCIAL ENGINEERING
    # --------------------------------------------------

    social_patterns = [

        "fake identity",
        "pretend to be",
        "impersonate",
        "pose as",
        "act as support"
    ]

    # --------------------------------------------------
    # CREDENTIAL THEFT
    # --------------------------------------------------

    credential_patterns = [

        "account password",
        "steal password",
        "get password",
        "login credentials",
        "steal credentials"
    ]

    # --------------------------------------------------
    # HARASSMENT
    # --------------------------------------------------

    harassment_patterns = [

        "harass",
        "bully",
        "keep bothering",
        "insult repeatedly",
        "target repeatedly"
    ]

    # --------------------------------------------------
    # COERCION
    # --------------------------------------------------

    coercion_patterns = [

        "force you",
        "make you do",
        "threaten until",
        "pressure you",
        "compel you"
    ]

    # --------------------------------------------------
    # FRAUD
    # --------------------------------------------------

    fraud_patterns = [

        "otp dao",
        "send otp",
        "bank password",
        "credit card pin",
        "verification code"
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

    for pattern in social_patterns:
        if pattern in text:
            intents.append("social_engineering")

    for pattern in credential_patterns:
        if pattern in text:
            intents.append("credential_theft")

    for pattern in harassment_patterns:
        if pattern in text:
            intents.append("harassment")

    for pattern in coercion_patterns:
        if pattern in text:
            intents.append("coercion")

    for pattern in fraud_patterns:
        if pattern in text:
            intents.append("fraud")

    for pattern in safe_patterns:
        if pattern in text:
            intents.append("non-malicious")

    # --------------------------------------------------
    # REMOVE DUPLICATES
    # --------------------------------------------------

    intents = list(dict.fromkeys(intents))

    # --------------------------------------------------
    # REMOVE CONTRADICTORY SAFE LABEL
    # --------------------------------------------------

    HIGH_RISK_INTENTS = {
        "violent_threat",
        "cyber_intrusion",
        "fraud",
        "credential_theft",
        "social_engineering",
    }

    if (
        "non-malicious" in intents and
        any(intent in HIGH_RISK_INTENTS for intent in intents)
    ):
        intents.remove("non-malicious")

    # --------------------------------------------------
    # DEFAULT
    # --------------------------------------------------

    if not intents:
        intents.append("unknown_or_safe")

    return intents
