def classify_intent(text):

    text = text.lower()

    intents = []

    violent_patterns = [
        "mere felbo",
        "mar dunga",
        "sesh kore dibo",
        "kill you",
        "dekhe nibo"
    ]

    cyber_patterns = [
        "hack the system",
        "breach server"
    ]

    safe_patterns = [
        "sleep schedule"
    ]

    for pattern in violent_patterns:
        if pattern in text:
            intents.append("violent_threat")

    for pattern in cyber_patterns:
        if pattern in text:
            intents.append("cyber_intrusion")

    for pattern in safe_patterns:
        if pattern in text:
            intents.append("non-malicious")

    if not intents:
        intents.append("unknown_or_safe")

    return intents
