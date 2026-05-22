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
# SYSTEM MODE
# --------------------------------------------------

SYSTEM_MODE = "Hybrid-Light"
SYSTEM_VERSION = "9.0.0"

# --------------------------------------------------
# SAFE CONTEXTS
# --------------------------------------------------

SAFE_CONTEXTS = [

    # productivity / self-improvement
    "hack my sleep schedule",
    "sleep schedule",
    "study hack",
    "life hack",
    "productivity hack",

    # gaming
    "game strategy",
    "gaming strategy",

    # harmless expressions
    "kill time",
    "destroy boredom"
]

# --------------------------------------------------
# MULTILINGUAL RISK SIGNALS
# --------------------------------------------------

MULTI_LANG_RISK = {

    # ==================================================
    # CYBER / EXPLOIT
    # ==================================================

    "hack": [

        # English
        "hack",
        "hack the system",
        "bypass security",
        "exploit vulnerability",
        "break firewall",
        "steal data",

        # variations
        "haek",
        "hek",
        "hax",

        # Banglish
        "system hack korbo",
        "security bypass korbo",
        "data churi korbo",
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
    ],

    # ==================================================
    # VIOLENCE / THREAT
    # ==================================================

    "violence": [

        # ---------------- ENGLISH ----------------

        "kill",
        "kill you",
        "i will kill you",
        "murder",
        "murder you",
        "burn",
        "destroy you",

        # ---------------- BANGLISH ----------------

        "mere felbo",
        "khun korbo",

        "shesh kore dibo",
        "shesh kore debo",

        "toke dekhe nibo",

        "ami toke marbo",
        "ami tomake mere felbo",

        # ---------------- BANGLA ----------------

        "মেরে ফেলবো",
        "খুন করবো",

        "শেষ করে দিব",
        "শেষ করে দেব",

        "উড়িয়ে দিব",
        "ধ্বংস করে দিব",

        "তোকে দেখে নিব",

        "আমি তোকে মারবো",
        "আমি তোকে মেরে ফেলবো",

        # ---------------- HINDI ----------------

        "maar dunga",
        "jaan se mar dunga",
        "tujhe mar dunga",
        "tujhe maar dunga",
        "tujhe khatam kar dunga"
    ]
}

# --------------------------------------------------
# LIGHTWEIGHT BEHAVIOR TRIGGERS
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
