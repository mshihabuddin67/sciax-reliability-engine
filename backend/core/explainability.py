def generate_explanations(text):

    explanations = []

    text = text.lower().strip()

    # ==================================================
    # SAFE CONTEXT FIRST (PRIORITY)
    # ==================================================

    safe_patterns = [

        "sleep schedule",
        "study hack",
        "life hack",
        "productivity hack",
        "game strategy"
    ]

    for pattern in safe_patterns:

        if pattern in text:

            explanations.append(
                "safe contextual usage detected"
            )

            return explanations

    # ==================================================
    # VIOLENT INTENT DETECTION
    # ==================================================

    violent_patterns = [

        # English
        "kill",
        "murder",
        "destroy you",

        # Banglish
        "mere felbo",
        "khun korbo",
        "shesh kore dibo",
        "shesh kore debo",

        # Bangla
        "শেষ করে দিব",
        "শেষ করে দেব",
        "মেরে ফেলবো",
        "খুন করবো",

        # Hindi
        "mar dunga",
        "maar dunga",
        "tujhe mar dunga",
        "tujhe maar dunga",
        "tujhe khatam kar dunga"
    ]

    for pattern in violent_patterns:

        if pattern in text:

            explanations.append(
                "violent intent structure detected"
            )

            break

    # ==================================================
    # IMPLICIT THREAT ESCALATION
    # ==================================================

    escalation_patterns = [

        "toke dekhe nibo",
        "dekhe nibo",

        "শেষ করে দিব",
        "শেষ করে দেব",

        "tujhe dekh lunga",
        "dekh lunga"
    ]

    for pattern in escalation_patterns:

        if pattern in text:

            explanations.append(
                "implicit threat escalation detected"
            )

            break

    # ==================================================
    # CYBER ABUSE DETECTION
    # ==================================================

    cyber_patterns = [

        "hack the system",
        "bypass security",
        "exploit vulnerability",
        "steal data",
        "breach server",

        "system hack korbo",
        "data churi korbo"
    ]

    for pattern in cyber_patterns:

        if pattern in text:

            explanations.append(
                "cyber abuse pattern detected"
            )

            break

    # ==================================================
    # DEFAULT FALLBACK
    # ==================================================

    if not explanations:

        explanations.append(
            "normal interaction pattern detected"
        )

    return explanations
