"""
Cross-script multilingual patterns for S-CIAX.

This module stores mixed-language and mixed-script expressions
where the same behavioral intent appears across Bangla, Hindi,
English, or Romanized forms.

Detection logic is implemented elsewhere.
"""

CROSS_SCRIPT_PATTERNS = [

    # Bangla + Hindi + English threat combination
    "তোকে ছাড়বো না, tujhe nahi chodunga",
    "tujhe nahi chodunga",
    "i know where you live",

    # Bangla + Hindi mixed
    "শেষ দেখে নিবো",
    "tera anjaam bura hoga",
    "toke charbo na",

    # Romanized multilingual
    "toke charbo na",
    "tujhe nahi chhodunga",
    "ami jani where you live",

    # Threat + location targeting
    "address ta jani",
    "where you live",
    "tomar location jani",

    # Mixed cyber examples
    "system hack korbo",
    "login info dao",
    "password de do",

]
