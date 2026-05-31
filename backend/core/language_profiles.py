def detect_language_profile(text):

    # ----------------------------------
    # Bangla Script
    # ----------------------------------

    if any("\u0980" <= c <= "\u09FF" for c in text):

        return ["Bangla"]

    # ----------------------------------
    # Hindi Script
    # ----------------------------------

    if any("\u0900" <= c <= "\u097F" for c in text):

        return ["Hindi"]

    text_lower = text.lower()

    # ----------------------------------
    # Romanized Bangla
    # ----------------------------------

    roman_bangla_markers = [

        "toke",
        "tore",
        "tomake",
        "ami",

        "shesh",
        "sesh",
        "mere",
        "felbo",

        "marbo",
        "khun",

        "dibo",
        "debo",

        "korbo",
        "kore",

        "nibo",
        "nebo"
    ]

    if any(
        marker in text_lower
        for marker in roman_bangla_markers
    ):

        return ["Romanized Bangla"]

    # ----------------------------------
    # Roman Hindi
    # ----------------------------------

    roman_hindi_markers = [

        "tujhe",
        "tumhe",
        "mujhe",

        "mar dunga",
        "maar dunga",

        "khatam kar dunga",

        "dekh lunga",

        "karunga",
        "nahi"
    ]

    if any(
        marker in text_lower
        for marker in roman_hindi_markers
    ):

        return ["Roman Hindi"]

    # ----------------------------------
    # Default
    # ----------------------------------

    return ["English"]
