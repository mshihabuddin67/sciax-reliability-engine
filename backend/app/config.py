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
    "destroy boredom",
]

# --------------------------------------------------
# VIOLENCE / THREAT DETECTION
# --------------------------------------------------

VIOLENCE_STRONG = [

    # ---------------- ENGLISH ----------------

    "kill you",
    "i will kill you",
    "murder you",
    "destroy you",
    "burn you",

    # ---------------- BANGLISH ----------------

    "ami toke marbo",
    "ami toke mere felbo",

    "toke khun korbo",

    "shesh kore dibo",
    "shesh kore debo",

    "toke shesh kore dibo",
    "toke shesh kore debo",

    "toke dekhe nibo",

    "khun korbo",

    "mere felbo",
    
    # ---------------- BANGLA ----------------

    "আমি তোকে মারবো",
    "আমি তোকে মেরে ফেলবো",

    "তোকে খুন করবো",

    "তোকে দেখে নিব",

    "শেষ করে দিব",
    "শেষ করে দেব",

    "তোকে শেষ করে দিব",
    "তোকে শেষ করে দেব",

    "উড়িয়ে দিব",
    "ধ্বংস করে দিব",
    "খুন করবো",
    "মেরে ফেলবো",
    
    # ---------------- HINDI ----------------

    "maar dunga",
    "jaan se mar dunga",

    "tujhe mar dunga",
    "tujhe maar dunga",

    "tujhe khatam kar dunga",
]

# --------------------------------------------------
# CYBER / EXPLOIT DETECTION
# --------------------------------------------------

CYBER_STRONG = [

    # ---------------- ENGLISH ----------------

    "hack the system",
    "bypass security",
    "steal data",
    "exploit vulnerability",
    "break firewall",

    "breach server",
    
    # ---------------- BANGLISH ----------------

    "system hack korbo",
    "data churi korbo",
    "security bypass korbo",
    "system bhangbo",

    # ---------------- BANGLA ----------------

    "সিস্টেম হ্যাক করবো",
    "ডাটা চুরি করবো",
    "সিকিউরিটি ভাঙবো",
    "সিস্টেম ধ্বংস করবো",

    # ---------------- HINDI ----------------

    "system hack karunga",
    "data churaunga",
    "security tod dunga",
]

# ==================================================
# FRAUD DETECTION
# ==================================================

FRAUD_STRONG = [
    "otp",
    "otp dao",
    "send otp",
    "bank password",
    "credit card pin",
    "verification code",
]

# --------------------------------------------------
# MULTILINGUAL RISK SIGNALS
# --------------------------------------------------

MULTI_LANG_RISK = {

    "hack": CYBER_STRONG,

    "violence": VIOLENCE_STRONG
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
