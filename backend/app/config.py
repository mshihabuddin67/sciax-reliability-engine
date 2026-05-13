# ----------------------------
# S-CIAX CONFIGURATION
# ----------------------------

API_NAME = "S-CIAX Engine"
VERSION = "1.1.0"

API_KEYS = {
    "sciax-demo-key-123": "demo-user"
}

# Default scores
DEFAULT_STABILITY = 0.9
DEFAULT_CONFLICT = 0.1
DEFAULT_RISK = "Low"

# Thresholds
HIGH_RISK_THRESHOLD = 0.75
MEDIUM_RISK_THRESHOLD = 0.5

# ----------------------------
# MULTILINGUAL RISK MAP
# ----------------------------
MULTI_LANG_RISK = {

    "hack": [
        "hack", "attack", "exploit",
        "সিস্টেম হ্যাক", "আক্রমণ", "सिस्टम तोड़ना", "हमला"
    ],

    "steal": [
        "steal", "rob", "theft",
        "চুরি", "ডাটা চুরি", "चोरी"
    ],

    "malware": [
        "malware", "virus", "trojan"
    ]
}

# System mode
DEBUG_MODE = True
