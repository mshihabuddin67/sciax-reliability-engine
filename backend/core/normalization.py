import re


def normalize_text(text):

    text = text.lower().strip()

    # ----------------------------------
    # Character substitutions
    # ----------------------------------

    replacements = {

        "@": "a",
        "0": "o",
        "1": "i",
        "3": "e",
        "$": "s",
        "5": "s",
        "!": "i",
        "7": "t"
    }

    for old, new in replacements.items():

        text = text.replace(
            old,
            new
        )

    # ----------------------------------
    # Remove repeated chars
    # e.g. maaaarbo -> marbo
    # ----------------------------------

    text = re.sub(
        r"(.)\1{2,}",
        r"\1",
        text
    )

    # ----------------------------------
    # Remove special chars
    # ----------------------------------

    text = re.sub(
        r"[^a-zA-Z0-9\u0980-\u09FF\u0900-\u097F\s]",
        " ",
        text
    )

    # ----------------------------------
    # Normalize spacing
    # ----------------------------------

    text = re.sub(
        r"\s+",
        " ",
        text
    ).strip()

    # ----------------------------------
    # Reconstruct fragmented words
    # ----------------------------------

    reconstructions = {

        "m a r b o": "marbo",
        "k i l l": "kill",
        "m a r d u n g a": "mar dunga",

        "s h e s h": "shesh",
        "s e s h": "sesh",

        "d i b o": "dibo",
        "d e b o": "debo",

        "t o k e": "toke",
        "t o m a k e": "tomake"
    }

    for old, new in reconstructions.items():

        text = text.replace(
            old,
            new
        )

    # ----------------------------------
    # Romanized Bangla fixes
    # ----------------------------------

    text = text.replace(
        "koredibo",
        "kore dibo"
    )

    text = text.replace(
        "koredebo",
        "kore debo"
    )

    text = text.replace(
        "sheshkore",
        "shesh kore"
    )

    return text
