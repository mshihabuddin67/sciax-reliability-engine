# ==================================================
# S-CIAX CONFIGURATION
# ==================================================

API_KEYS = [
    "sciax-demo-key-123"
]

# --------------------------------------------------
# DEFAULT VALUES
# --------------------------------------------------

DEFAULT_STABILITY = 0.9
DEFAULT_CONFLICT = 0.1
DEFAULT_RISK = "Low"

# --------------------------------------------------
# MULTILINGUAL RISK DATASET
# --------------------------------------------------

VIOLENCE_STRONG = [

    # English
    "kill you",
    "i will kill you",
    "murder you",
    "destroy you",

    # Banglish
    "ami toke marbo",
    "ami toke mere felbo",
    "toke khun korbo",
    "toke shesh kore dibo",
    "toke dekhe nibo",

    # Bangla
    "আমি তোকে মারবো",
    "আমি তোকে মেরে ফেলবো",
    "তোকে খুন করবো",
    "তোকে দেখে নিব",

    # Hindi
    "tujhe maar dunga",
    "tujhe mar dunga",
    "tujhe khatam kar dunga"
]

# --------------------------------------------------

CYBER_STRONG = [

    # English
    "hack the system",
    "bypass security",
    "steal data",
    "exploit vulnerability",

    # Banglish
    "system hack korbo",
    "data churi korbo",
    "system bhangbo",

    # Bangla
    "সিস্টেম হ্যাক করবো",
    "ডাটা চুরি করবো",
    "সিকিউরিটি ভাঙবো",

    # Hindi
    "system hack karunga",
    "data churaunga"
]

# --------------------------------------------------

BEHAVIOR_TRIGGERS = [

    "toke",
    "tui",
    "tujhe",
    "tomake",

    "marbo",
    "kill",
    "khun",
    "destroy",

    "dekhe nibo",
    "shesh kore dibo"
]
