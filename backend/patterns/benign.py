"""
Benign / safe interaction patterns for S-CIAX.

This module stores common harmless expressions,
collaboration language, learning context, social interaction,
and positive figurative language.

Used for false-positive reduction and safe classification.

Detection logic is implemented elsewhere.
"""

BENIGN_PATTERNS = [

    # ==================================
    # Learning / education context
    # ==================================

    "class e",
    "class er",
    "assignment",
    "homework",
    "project",
    "research",
    "study",
    "porashona",
    "notes share",
    "notes dao",
    "lecture",
    "exam preparation",
    "exam er jonno",
    "practice kori",


    # ==================================
    # Productivity context
    # ==================================

    "productivity hack",
    "study hack",
    "life hack",
    "time management",
    "routine improve",
    "better workflow",
    "planning",
    "goal set kora",
    "skill improve",


    # ==================================
    # Friendly social interaction
    # ==================================

    "coffee khabo",
    "coffee khete jabo",
    "dekha korte chai",
    "tomar sathe dekha hobe",
    "bondhu",
    "bro",
    "friend",
    "hello",
    "hi",
    "kemon acho",

    "onek din por dekha",
    "valo theko",
    "take care",


    # ==================================
    # Positive expressions
    # ==================================

    "great job",
    "well done",
    "nice work",
    "excellent",
    "awesome",
    "amazing",

    "killer presentation",
    "killer idea",
    "killer design",
    "best performance",


    # ==================================
    # Help / collaboration
    # ==================================

    "help lagbe",
    "help korte parba",
    "ekta suggestion dao",
    "idea share koro",
    "feedback dao",
    "review kore dao",

    "project e help chai",
    "team work",
    "group project",


    # ==================================
    # Normal requests
    # ==================================

    "information dao",
    "explain koro",
    "bujhiye bolo",
    "ki vabe korbo",
    "tutorial chai",
    "example dao",

    # ==================================
    # Bengali safe phrases
    # ==================================

    "valo acho",
    "ki khobor",
    "dhonnobad",
    "onek valo",
    "shubho din",

]
