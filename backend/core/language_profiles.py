def detect_language_profile(text):

    if any("\u0980" <= c <= "\u09FF" for c in text):
        return ["Bangla"]

    text_lower = text.lower()

    if "tore" in text_lower or "nibo" in text_lower:
        return ["Roman Bangla"]

    if "mar dunga" in text_lower:
        return ["Roman Hindi"]

    return ["English"]
