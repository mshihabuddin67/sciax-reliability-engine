# ==================================================
# S-CIAX EXPLAINABILITY ENGINE
# ==================================================

def generate_explanations(text):

    explanations = []

    text = text.lower().strip()

    # ==================================================
    # SAFE CONTEXT FIRST (TOP PRIORITY)
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
    # DIRECT VIOLENT PHRASE MATCH
    # ==================================================

    violent_patterns = [

        # English
        "kill",
        "kill you",
        "murder",
        "destroy you",

        # Banglish
        "mere felbo",
        "khun korbo",
        "shesh kore dibo",
        "shesh kore debo",

        # Bangla Unicode
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
                "direct violent phrase match detected"
            )

            break

    # ==================================================
    # TARGET-DIRECTED AGGRESSION
    # ==================================================

    target_patterns = [

        "toke",
        "tomake",
        "tujhe",
        "you"
    ]

    aggression_patterns = [

        "mar",
        "kill",
        "destroy",
        "shesh",
        "khatam"
    ]

    if any(t in text for t in target_patterns) and any(
        a in text for a in aggression_patterns
    ):

        explanations.append(
            "target-directed aggression identified"
        )

    # ==================================================
    # IMPLICIT THREAT ESCALATION
    # ==================================================

    escalation_patterns = [

        "toke dekhe nibo",
        "dekhe nibo",

        "শেষ করে দিব",
        "শেষ করে দেব",

        "tujhe dekh lunga",
        "dekh lunga",

        "shesh kore dibo",
        "shesh kore debo"
    ]

    for pattern in escalation_patterns:

        if pattern in text:

            explanations.append(
                "implicit threat escalation detected"
            )

            break

    # ==================================================
    # MULTILINGUAL THREAT STRUCTURE
    # ==================================================

    multilingual_patterns = [

        "mar dunga",
        "mere felbo",
        "shesh kore dibo",
        "শেষ করে দিব"
    ]

    for pattern in multilingual_patterns:

        if pattern in text:

            explanations.append(
                "multilingual violent intent structure detected"
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
    # FIRST-PERSON THREAT LANGUAGE
    # ==================================================

    first_person_patterns = [

        "i will",
        "ami",
        "mar dunga",
        "mere felbo",
        "shesh kore dibo"
    ]

    for pattern in first_person_patterns:

        if pattern in text:

            explanations.append(
                "first-person threat language detected"
            )

            break

    # ==================================================
    # DEFAULT FALLBACK
    # ==================================================

    if not explanations:

        explanations.append(
            "normal interaction pattern detected"
        )

    # ==================================================
    # REMOVE DUPLICATES
    # ==================================================

    explanations = list(
        dict.fromkeys(explanations)
    )

    return explanations
