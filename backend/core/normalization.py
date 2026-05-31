import re


def normalize_text(text):

    text = text.lower().strip()

    # ----------------------------------
    # SYMBOL → LETTER SUBSTITUTION
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
        text = text.replace(old, new)

    # ----------------------------------
    # REMOVE EXTRA REPETITIONS
    # e.g. maaaaarbo → marbo
    # ----------------------------------

    text = re.sub(r"(.)\1{2,}", r"\1", text)

    # ----------------------------------
    # REMOVE SPECIAL CHARACTERS
    # ----------------------------------

    text = re.sub(
        r"[^a-zA-Z0-9\u0980-\u09FF\u0900-\u097F\s]",
        " ",
        text
    )

    # ----------------------------------
    # NORMALIZE WHITESPACE
    # ----------------------------------

    text = re.sub(r"\s+", " ", text).strip()

    # ----------------------------------
    # WORD RECONSTRUCTION (FRAGMENTED TEXT)
    # ----------------------------------

    reconstructions = {

        "m a r b o": "marbo",
        "k i l l": "kill",
        "m a r d u n g a": "mar dunga",

        "s h e s h": "shesh",
        "s e s h": "shesh",

        "d i b o": "dibo",
        "d e b o": "debo",

        "t o k e": "toke",
        "t o m a k e": "tomake",

        "d e k h e": "dekhe",
        "n i b o": "nibo"
    }

    for old, new in reconstructions.items():
        text = text.replace(old, new)

    # ----------------------------------
    # ROMANIZED BANGLA NORMALIZATION FIXES
    # ----------------------------------

    fixes = {

        "koredibo": "kore dibo",
        "koredebo": "kore debo",
        "sheshkore": "shesh kore",
        "dekhenibo": "dekhe nibo",
        "marboi": "marbo",
        "marbooo": "marbo"
    }

    for old, new in fixes.items():
        text = text.replace(old, new)

    # ----------------------------------
    # FINAL CLEANUP
    # ----------------------------------

    text = re.sub(r"\s+", " ", text).strip()

    return text
