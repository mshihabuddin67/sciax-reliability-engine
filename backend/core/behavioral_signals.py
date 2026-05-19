def detect_behavioral_signals(text):

    text = text.lower()

    signals = []

    if "dekhe nibo" in text:
        signals.append("target-oriented hostility")
        signals.append("implicit threat escalation")

    if "mar dunga" in text:
        signals.append("violent aggression")

    if "sesh kore dibo" in text:
        signals.append("direct violent hostility")

    if "hack the system" in text:
        signals.append("cyber intrusion intent")

    if "hack my sleep schedule" in text:
        signals.append("benign optimization context")

    return signals
