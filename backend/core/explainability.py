def generate_explanations(text):

    explanations = []

    text = text.lower()

    # -----------------------------------
    # Threat signals
    # -----------------------------------

    if (
        "kill" in text or
        "murder" in text or
        "mere felbo" in text or
        "khun korbo" in text
    ):

        explanations.append(
            "violent intent structure detected"
        )

    # -----------------------------------
    # Threat escalation
    # -----------------------------------

    if (
        "toke dekhe nibo" in text or
        "dekhe nibo" in text
    ):

        explanations.append(
            "implicit threat escalation detected"
        )

    # -----------------------------------
    # Cyber abuse
    # -----------------------------------

    if (
        "hack" in text or
        "bypass" in text or
        "exploit" in text
    ):

        explanations.append(
            "cyber abuse pattern detected"
        )

    # -----------------------------------
    # Safe context
    # -----------------------------------

    if (
        "sleep schedule" in text or
        "study hack" in text or
        "life hack" in text
    ):

        explanations.append(
            "safe contextual usage detected"
        )

    # -----------------------------------
    # Default
    # -----------------------------------

    if not explanations:

        explanations.append(
            "normal interaction pattern detected"
        )

    return explanations
