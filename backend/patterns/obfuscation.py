"""
Obfuscation and evasion patterns for S-CIAX.

This module stores common character substitution,
leetspeak, spacing manipulation, and disguised malicious
expressions.

Detection logic is implemented elsewhere.
"""

OBFUSCATION_PATTERNS = [

    # ==================================
    # Violence obfuscation
    # ==================================

    "m@re",
    "m@rbo",
    "m4re",
    "m4rbo",
    "mere",
    "fel@bo",
    "f3labo",
    "f3lbo",
    "k!ll",
    "k1ll",
    "k1l",
    "kill3r",

    "m@r3 felbo",
    "mere fel@bo",
    "t0ke m@re felbo",
    "t0ke shesh kore dibo",


    # ==================================
    # Threat phrase mutation
    # ==================================

    "t0ke",
    "t0kay",
    "t0r",
    "t@ke",
    "ch@rbo",
    "charb0",
    "chodung@",
    "ch0dunga",

    "dekhe n3bo",
    "d3khbo",
    "sh3sh",
    "sh3sh kore dibo",


    # ==================================
    # Cyber obfuscation
    # ==================================

    "h@ck",
    "h4ck",
    "hack3r",
    "h@cker",
    "h4cker",

    "l0gin",
    "log1n",
    "l0g1n",
    "passw0rd",
    "p@ssword",
    "p4ssword",

    "cred3ntial",
    "cr3dential",
    "access",
    "acc3ss",

    "syst3m hack",
    "s!stem hack",
    "sys@tem hack",


    # ==================================
    # Credential theft obfuscation
    # ==================================

    "0tp",
    "0t3p",
    "otp dao",
    "0tp dao",
    "verification c0de",

    "pin c0de",
    "cvv c0de",
    "bank l0gin",
    "account acc3ss",


    # ==================================
    # Social engineering mutation
    # ==================================

    "adm1n",
    "@dmin",
    "support t3am",
    "hr t3am",

    "verific@tion",
    "confirm@tion",
    "auth3ntication",


    # ==================================
    # Symbol / spacing variants
    # ==================================

    "h a c k",
    "h-a-c-k",
    "h_a_c_k",

    "p a s s w o r d",
    "p@ ssw0rd",
    "pa$$word",

    "l o g i n",
    "otp-code",
    "otp_code",


    # ==================================
    # Mixed language obfuscation
    # ==================================

    "hack kor@ dibo",
    "system h@ck korbo",
    "login info d3",

    "password d@o",
    "otp b0le dao",
    "access d@o",

]
