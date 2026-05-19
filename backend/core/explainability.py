def generate_explainability(text):

    text = text.lower()

    explanations = []

    if "dekhe nibo" in text:
        explanations.append(
            "implicit threat structure identified"
        )

        explanations.append(
            "target-directed phrasing detected"
        )

    if "hack the system" in text:
        explanations.append(
            "unauthorized system access intent identified"
        )

    if "mar dunga" in text:
        explanations.append(
            "violent aggression pattern recognized"
        )

    if "sesh kore dibo" in text:
        explanations.append(
            "direct violent intent pattern identified"
        )

    if "sleep schedule" in text:
        explanations.append(
            "non-harmful contextual usage identified"
        )

    return explanations
