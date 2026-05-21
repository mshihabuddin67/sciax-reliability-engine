# ==================================================
# S-CIAX CONFIG v9 STABLE
# ==================================================

# --------------------------------------------------
# API KEYS
# --------------------------------------------------

API_KEYS = [
    "sciax-demo-key-123"
]

# --------------------------------------------------
# DEFAULT SYSTEM VALUES
# --------------------------------------------------

DEFAULT_STABILITY = 0.9
DEFAULT_CONFLICT = 0.1
DEFAULT_RISK = "Low"

HIGH_RISK_THRESHOLD = 0.75
MEDIUM_RISK_THRESHOLD = 0.55

# --------------------------------------------------
# VIOLENCE / THREAT DETECTION
# --------------------------------------------------

VIOLENCE_STRONG = [

    # English
    "kill you",
    "i will kill you",
    "murder you",
    "destroy you",
    "burn you",

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
    "তোকে শেষ করে দিব",

    # Hindi
    "tujhe maar dunga",
    "tujhe mar dunga",
    "tujhe khatam kar dunga"
]

# --------------------------------------------------
# CYBER / EXPLOIT DETECTION
# --------------------------------------------------

CYBER_STRONG = [

    # English
    "hack the system",
    "bypass security",
    "steal data",
    "exploit vulnerability",
    "break firewall",

    # Banglish
    "system hack korbo",
    "data churi korbo",
    "security bypass korbo",
    "system bhangbo",

    # Bangla
    "সিস্টেম হ্যাক করবো",
    "ডাটা চুরি করবো",
    "সিকিউরিটি ভাঙবো",
    "সিস্টেম ধ্বংস করবো",

    # Hindi
    "system hack karunga",
    "data churaunga",
    "security tod dunga"
]

# --------------------------------------------------
# BEHAVIOR SIGNALS (LIGHTWEIGHT CONTEXT HELP)
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
