import re


def normalize_text(text):

    text = text.lower().strip()

    replacements = {
        "@": "a",
        "0": "o",
        "1": "i",
        "3": "e",
        "$": "s",
        "5": "s"
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    # Remove repeated characters
    text = re.sub(r"(.)\1{2,}", r"\1", text)

    # Remove excessive spacing
    text = re.sub(r"\s+", " ", text)

    # Reconstruct fragmented words
    text = text.replace("m a r b o", "marbo")
    text = text.replace("k i l l", "kill")

    return text
