"""
Contextual and implicit threat patterns for S-CIAX.

This module stores indirect threat indicators where intent
is expressed through implication, intimidation, warning,
or future harm suggestion.

Detection logic is implemented elsewhere.
"""

CONTEXTUAL_THREAT_PATTERNS = [

    # Indirect warning
    "valo hobe na tomar jonno",
    "bhalo hobe na",
    "mone rakhis",
    "dekhe nebo",
    "dekha hobe",
    "wait korchi tor jonno",

    # Personal targeting indicators
    "tor address jani",
    "where you live",
    "tomake khuje ber korbo",
    "tomar sathe dekha korbo",

    # Time pressure / escalation
    "somoy khub kom",
    "time nei tomar",
    "last warning",
    "eta mone rakhis",

    # Bengali / Romanized Bengali
    "toke charbo na",
    "chere dibo na",
    "shesh dekhe nibo",

    # Hindi / mixed context
    "tera anjaam bura hoga",
    "tujhe nahi chodunga",

]
