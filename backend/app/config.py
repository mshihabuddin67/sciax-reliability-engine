# --------------------------------------------------
# API KEYS
# --------------------------------------------------

API_KEYS = [
    "sciax-demo-key-123"
]

# --------------------------------------------------
# DEFAULT VALUES
# --------------------------------------------------

DEFAULT_STABILITY = 0.9
DEFAULT_CONFLICT = 0.1
DEFAULT_RISK = "Low"

HIGH_RISK_THRESHOLD = 0.8
MEDIUM_RISK_THRESHOLD = 0.5

# --------------------------------------------------
# MULTILINGUAL RISK SIGNALS
# --------------------------------------------------

MULTI_LANG_RISK = {

    # --------------------------------------------------
    # CYBER / EXPLOIT
    # --------------------------------------------------

    "hack": [

        "hack",
        "haek",
        "hek",
        "hax",

        "bypass",
        "exploit",

        "system bhangbo",
        "destroy system",

        "data churi",
        "steal data"
    ],

    # --------------------------------------------------
    # VIOLENCE
    # --------------------------------------------------

    "violence": [

        # english
        "kill",
        "murder",
        "burn",
        "destroy you",

        # banglish
        "mere felbo",
        "khun korbo",

        "shesh kore dibo",
        "shesh kore debo",

        "toke dekhe nibo",

        # bangla unicode
        "মেরে ফেলবো",
        "খুন করবো",

        "শেষ করে দিব",
        "শেষ করে দেব",

        "উড়িয়ে দিব",
        "ধ্বংস করে দিব",

        "তোকে দেখে নিব",

        # hindi
        "maar dunga",
        "jaan se mar dunga"
    ]
}

# --------------------------------------------------
# SYSTEM MODE
# --------------------------------------------------

SYSTEM_MODE = "Hybrid-Light"
SYSTEM_VERSION = "9.0.0"
