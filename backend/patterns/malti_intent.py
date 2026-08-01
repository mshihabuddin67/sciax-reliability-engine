"""
Multi-intent behavioral patterns for S-CIAX.

This module stores combinations where multiple risk signals
appear together in the same interaction.

Examples:
- Threat + credential request
- Fraud + coercion
- Cyber + intimidation

Detection logic is implemented elsewhere.
"""

MULTI_INTENT_PATTERNS = [

    # ==================================
    # Credential theft + threat
    # ==================================

    "password dao na hole",
    "otp dao na hole",
    "login info dao na hole",
    "credentials dao nahole",

    "access dao nahole dekhe nibo",
    "password na dile valo hobe na",


    # ==================================
    # Cyber + coercion
    # ==================================

    "system hack kore dibo",
    "account hack kore dibo",
    "login nosto kore dibo",

    "hack korbo jodi na dao",
    "system e dhukbo jodi na dao",


    # ==================================
    # Fraud + urgency + pressure
    # ==================================

    "ekhoni verification dao",
    "urgent otp dao",
    "taratari password dao",

    "account confirm koro ekhoni",
    "delay korle problem hobe",


    # ==================================
    # Threat escalation phrases
    # ==================================

    "na hole dekhe nibo",
    "na dile valo hobe na",
    "tarpor bujhbe",

    "last warning",
    "eta tomar jonno valo hobe na",


    # ==================================
    # Mixed language examples
    # ==================================

    "password dao nahi to dekh lena",
    "otp do warna problem hoga",
    "login info dao nahole shesh",

]
