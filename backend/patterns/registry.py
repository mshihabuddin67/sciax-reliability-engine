"""
S-CIAX Pattern Registry

Central loader for all modular behavioral patterns.

This file combines patterns from individual modules.
Detection logic is implemented elsewhere.
"""

from .violence import VIOLENCE_PATTERNS
from .cyber import CYBER_PATTERNS
from .fraud import FRAUD_PATTERNS
from .social_engineering import SOCIAL_ENGINEERING_PATTERNS
from .contextual_threats import CONTEXTUAL_THREAT_PATTERNS
from .cross_script import CROSS_SCRIPT_PATTERNS
from .obfuscation import OBFUSCATION_PATTERNS
from .sarcasm import SARCASM_PATTERNS
from .ambiguity import AMBIGUITY_PATTERNS
from .multi_intent import MULTI_INTENT_PATTERNS
from .benign import BENIGN_PATTERNS


PATTERN_REGISTRY = {

    "violence": VIOLENCE_PATTERNS,

    "cyber": CYBER_PATTERNS,

    "fraud": FRAUD_PATTERNS,

    "social_engineering": SOCIAL_ENGINEERING_PATTERNS,

    "contextual_threats": CONTEXTUAL_THREAT_PATTERNS,

    "cross_script": CROSS_SCRIPT_PATTERNS,

    "obfuscation": OBFUSCATION_PATTERNS,

    "sarcasm": SARCASM_PATTERNS,

    "ambiguity": AMBIGUITY_PATTERNS,

    "multi_intent": MULTI_INTENT_PATTERNS,

    "benign": BENIGN_PATTERNS,

}
