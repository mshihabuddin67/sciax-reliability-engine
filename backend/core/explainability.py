def generate_explanations(text):

    explanations = []

    text = text.lower()

    # --------------------------------------------------
    # VIOLENT INTENT DETECTION
    # --------------------------------------------------

    if (
        "kill" in text or
        "murder" in text or
        "destroy you" in text or

        "mere felbo" in text or
        "khun korbo" in text or
        "shesh kore dibo" in text or
        "shesh kore debo" in text or

        "আমি তোকে মারবো" in text or
        "আমি তোমাকে শেষ করে দিব" in text or
        "মেরে ফেলবো" in text or
        "খুন করবো" in text or

        "mar dunga" in text or
        "tujhe mar dunga" in text
    ):

        explanations.append(
            "violent intent structure detected"
        )

    # --------------------------------------------------
    # IMPLICIT THREAT ESCALATION
    # --------------------------------------------------

    if (
        "toke dekhe nibo" in text or
        "dekhe nibo" in text or
        "শেষ করে দিব" in text or
        "shesh kore dibo" in text
    ):

        explanations.append(
            "implicit threat escalation detected"
        )

    # --------------------------------------------------
    # CYBER ABUSE DETECTION
    # --------------------------------------------------

    if (
        "hack" in text or
        "bypass" in text or
        "exploit" in text or

        "system hack korbo" in text or
        "data churi korbo" in text or
        "steal data" in text
    ):

        explanations.append(
            "cyber abuse pattern detected"
        )

    # --------------------------------------------------
    # SAFE CONTEXT DETECTION
    # --------------------------------------------------

    if (
        "sleep schedule" in text or
        "study hack" in text or
        "life hack" in text or
        "productivity hack" in text
    ):

        explanations.append(
            "safe contextual usage detected"
        )

    # --------------------------------------------------
    # DEFAULT FALLBACK
    # --------------------------------------------------

    if not explanations:

        explanations.append(
            "normal interaction pattern detected"
        )

    return explanations
