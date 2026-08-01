"""
Sarcasm and figurative language patterns for S-CIAX.

This module stores expressions that contain threat-like
words but are commonly used in harmless contexts.

Used for false-positive reduction.

Detection logic is implemented elsewhere.
"""

SARCASM_PATTERNS = [

    # ==================================
    # Friendly exaggeration
    # ==================================

    "mere felbi re pagol",
    "amake mere felbi",
    "marbo re",
    "toke mere dibo re",

    "tui sesh kore dili",
    "tui amake sesh kore dili",

    # ==================================
    # Exam / stress context
    # ==================================

    "exam e pressure",
    "exam er chap",
    "porashona pressure",
    "assignment er jonno morchi",

    "kal exam e mere dilo",
    "teacher mere dilo",

    # ==================================
    # Positive figurative words
    # ==================================

    "killer presentation",
    "killer performance",
    "killer idea",
    "killer design",

    "awesome attack",
    "great hit",

    # ==================================
    # Joke indicators
    # ==================================

    "joke chilo",
    "just kidding",
    "moja korchilam",
    "moja korchi",
    "seriously nio na",

    "don't take it seriously",
    "bro chill",

    # ==================================
    # Friendly conversation
    # ==================================

    "pagol",
    "re pagol",
    "bro",
    "bondhu",

    "tor sathe moja",
    "moja korlam",

]
