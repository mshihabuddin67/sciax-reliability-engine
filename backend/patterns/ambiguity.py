"""
Ambiguous context patterns for S-CIAX.

This module stores uncertain expressions that require
additional context before assigning a high-confidence risk level.

These patterns should not directly trigger blocking.

Detection logic is implemented elsewhere.
"""

AMBIGUITY_PATTERNS = [

    # ==================================
    # Emotional exhaustion
    # ==================================

    "amake chere de",
    "amake ekdom chere de",
    "r pari na",
    "ar parchi na",
    "ami klanto",

    "sob kichu sesh",
    "kichu valo lagche na",


    # ==================================
    # Indirect warning / uncertainty
    # ==================================

    "sabdhane thakis",
    "sabdhan thak",
    "sob somoy sob thik thake na",

    "dekha jak ki hoy",
    "ki hobe jani na",
    "somoy bole dibe",


    # ==================================
    # Conflict without clear threat
    # ==================================

    "amar sathe r kotha bolo na",
    "dur hoye ja",
    "amar theke dure thak",

    "eta mone rakhis",


    # ==================================
    # Context dependent phrases
    # ==================================

    "ami wait korchi",
    "tomar jonno opekkha korchi",
    "dekha hobe",

]
