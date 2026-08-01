"""
Social engineering related behavioral patterns for S-CIAX.

This module stores patterns where an attacker attempts to
manipulate trust, authority, urgency, or helpfulness to obtain
information or access.

Detection logic is implemented elsewhere.
"""

SOCIAL_ENGINEERING_PATTERNS = [

    # Authority impersonation
    "hr theke bolchi",
    "admin theke bolchi",
    "support theke bolchi",
    "bank theke bolchi",
    "official team",

    # Credential requests
    "credentials confirm koro",
    "login confirm koro",
    "password share koro",
    "otp bole dao",
    "verification code dao",
    "access dao",

    # Access manipulation
    "admin panel access",
    "account access",
    "temporary access",
    "remote access",

    # Urgency / pressure
    "urgent",
    "ekhoni korte hobe",
    "taratari dao",
    "time nei",
    "nahole problem hobe",

    # Mixed language examples
    "verification er jonno lagbe",
    "form e login details dao",
    "confirm your login",
]
