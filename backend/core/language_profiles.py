def detect_language_profile(text):

    languages = []
    
    # ----------------------------------
    # Bangla Script
    # ----------------------------------

    if any("\u0980" <= c <= "\u09FF" for c in text):
        languages.append("Bangla")
        

    # ----------------------------------
    # Hindi Script
    # ----------------------------------

    if any("\u0900" <= c <= "\u097F" for c in text):
        languages.append("Hindi")
        

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
        "nebo",
        
        "tomar",
        "tumi",
        
        "hoy",
        "mon",
        "dibe",
        "dibi",
        "koris",
        "morbi",
        "dekhis"
    ]

    if any(
        marker in text_lower
        for marker in roman_bangla_markers
    ):

        languages.append("Romanized Bangla")

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
        "nahi",
        "maar",
        "dunga",
        "mat"
    ]

    if any(
        marker in text_lower
        for marker in roman_hindi_markers
    ):

        languages.append("Roman Hindi")

    # ----------------------------------
    # English Detection
    # ----------------------------------

    english_markers = [
        "force",
        "release",
        "hack",
        "system",
        "sleep",
        "schedule",
        "you",
        "will"
    ]

    if any(
        marker in text_lower
        for marker in english_markers
    ):
        languages.append("English")

    # ----------------------------------
    # Final Output
    # ----------------------------------

    if not languages:
        languages.append("English")

    return list(dict.fromkeys(languages))
