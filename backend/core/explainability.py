# ==================================================
# S-CIAX EXPLAINABILITY ENGINE
# ==================================================

def generate_explanations(
    text,
    normalization_applied=False
):

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

            break

    # ==================================================
    # DIRECT VIOLENT PHRASE MATCH
    # ==================================================

    violent_patterns = [

        # English
        "kill you",
        "i will kill",
        "murder",
        "destroy you",

        # Romanized Bangla
        "mere felbo",
        "khun korbo",
        "shesh kore dibo",
        "shesh kore debo",

        # Bangla
        "শেষ করে দিব",
        "শেষ করে দেব",
        "মেরে ফেলবো",
        "খুন করবো",

        # Roman Hindi
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
        "tore",

        "tujhe",
        "tumhe",

        "kill you",
        "destroy you"
    ]

    aggression_patterns = [

        "mar",
        "kill",
        "destroy",
        "shesh",
        "khatam",
        "khun"
    ]

    if any(
        t in text
        for t in target_patterns
    ) and any(
        a in text
        for a in aggression_patterns
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

        "shesh kore dibo",
        "shesh kore debo",

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

            explanations.append(
                "malicious system access intent detected"
            )

            break

    # ==================================================
    # FRAUD DETECTION
    # ==================================================

    fraud_patterns = [

        "otp dao",
        "send otp",
        "bank password",
        "credit card pin",
        "verification code"
    ]

    for pattern in fraud_patterns:

        if pattern in text:

            explanations.append(
                "fraud-related information request detected"
            )

            break

    # ==================================================
    # SOCIAL ENGINEERING
    # ==================================================

    social_patterns = [

        "fake identity",
        "pretend to be",
        "impersonate",
        "pose as",
        "act as support"
    ]

    for pattern in social_patterns:

        if pattern in text:

            explanations.append(
                "social engineering behavior detected"
            )

            break

    # ==================================================
    # CREDENTIAL THEFT
    # ==================================================

    credential_patterns = [

        "account password",
        "steal password",
        "get password",
        "login credentials",
        "steal credentials"
    ]

    for pattern in credential_patterns:

        if pattern in text:

            explanations.append(
                "credential theft pattern detected"
            )

            break

    # ==================================================
    # HARASSMENT
    # ==================================================

    harassment_patterns = [

        "harass",
        "bully",
        "keep bothering",
        "insult repeatedly",
        "target repeatedly"
    ]

    for pattern in harassment_patterns:

        if pattern in text:

            explanations.append(
                "harassment behavior detected"
            )

            break

    # ==================================================
    # COERCION
    # ==================================================

    coercion_patterns = [

        "force you",
        "make you do",
        "threaten until",
        "pressure you",
        "compel you"
    ]

    for pattern in coercion_patterns:

        if pattern in text:

            explanations.append(
                "coercive behavior detected"
            )

            break

    # ==================================================
    # FIRST-PERSON THREAT LANGUAGE
    # ==================================================

    first_person_patterns = [

        "i will",
        "ami",

        "mar dunga",
        "maar dunga",

        "mere felbo",

        "shesh kore dibo",
        "shesh kore debo"
    ]

    for pattern in first_person_patterns:

        if pattern in text:

            explanations.append(
                "first-person threat language detected"
            )

            break

    # ==================================================
    # NORMALIZATION APPLIED
    # ==================================================

    if normalization_applied:

        explanations.append(
            "normalization match applied"
        )

    # ==================================================
    # DEFAULT FALLBACK
    # ==================================================

    if not explanations:

        explanations.append(
            "normal interaction pattern detected"
        )

    # ==================================================
    # REMOVE DUPLICATES (KEEP ORDER)
    # ==================================================

    explanations = list(
        dict.fromkeys(explanations)
    )

    return explanations
