"""
Fraud and financial deception related behavioral patterns for S-CIAX.

This module stores patterns related to phishing, credential theft,
financial scams, impersonation, and payment fraud.

Detection logic is implemented elsewhere.
"""

FRAUD_PATTERNS = [
    # Credential theft
    "one time password",
    "verification code",
    "password",
    "pin",
    "cvv",
    "security code",

    # Financial fraud
    "bank account",
    "bank login",
    "card number",
    "credit card",
    "debit card",
    "payment",
    "transaction",
    "otp",

    # Phishing / impersonation
    "verify your account",
    "confirm your account",
    "account verification",
    "login credentials",
    "admin access",
    "admin panel",
    "support team",
    "customer care",
    "hr",
    "steal credentials",
    
    # Mixed-language examples
    "otp dao",
    "password dao",
    "login credentials dao",
    "admin panel access",
    "verification er jonno",
    "bank password dao",
    
]
