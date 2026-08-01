"""
Cyber intrusion related behavioral patterns for S-CIAX.

This module stores keywords and phrases associated with
unauthorized system access, malware, exploitation,
and related cyber activities.

Detection logic is implemented elsewhere.
"""

CYBER_PATTERNS = [
    # Generic
    "hack",
    "hacking",
    "exploit",
    "payload",
    "malware",
    "virus",
    "trojan",
    "ransomware",
    "backdoor",
    "shell",
    "ddos",
    "botnet",

    # Credentials
    "login",
    "username",
    "password",
    "credential",
    "otp",
    "access token",
    "session cookie",

    # Mixed-language examples
    "system hack",
    "hack korbo",
    "hack kore dibo",
    "login info",
    "login details",
]
