"""
S-CIAX Contextual Safety Pattern Library

Purpose:
    Detect contextual patterns that can change the semantic interpretation
    of otherwise ambiguous or potentially risky language.

This module does NOT:
    - make final risk decisions
    - assign final severity
    - override the intent engine directly

It provides structured contextual evidence for downstream modules.

Context classes:
    1. benign_optimization
    2. defensive_security
    3. safe_general
    4. ambiguous_lexical

Design principle:
    A potentially risky keyword should not be treated as malicious
    without sufficient contextual evidence.
"""

from typing import Any, Dict, List


# ============================================================
# CONTEXTUAL SAFETY PATTERNS
# ============================================================

CONTEXTUAL_SAFETY_PATTERNS: List[Dict[str, Any]] = [

    # --------------------------------------------------------
    # 1. BENIGN OPTIMIZATION
    # --------------------------------------------------------

    {
        "pattern": "hack my sleep schedule",
        "context_type": "benign_optimization",
        "intent": "non-malicious",
        "strength": 0.95,
        "keywords": ["hack", "sleep", "schedule"],
        "explanation": "Optimization context involving sleep scheduling.",
    },

    {
        "pattern": "study hack",
        "context_type": "benign_optimization",
        "intent": "non-malicious",
        "strength": 0.90,
        "keywords": ["study", "hack"],
        "explanation": "Study or learning optimization context.",
    },

    {
        "pattern": "life hack",
        "context_type": "benign_optimization",
        "intent": "non-malicious",
        "strength": 0.95,
        "keywords": ["life", "hack"],
        "explanation": "General life-improvement context.",
    },

    {
        "pattern": "productivity hack",
        "context_type": "benign_optimization",
        "intent": "non-malicious",
        "strength": 0.95,
        "keywords": ["productivity", "hack"],
        "explanation": "Productivity optimization context.",
    },

    {
        "pattern": "study habits",
        "context_type": "benign_optimization",
        "intent": "non-malicious",
        "strength": 0.90,
        "keywords": ["study", "habits"],
        "explanation": "Educational self-improvement context.",
    },

    {
        "pattern": "game strategy",
        "context_type": "benign_optimization",
        "intent": "non-malicious",
        "strength": 0.90,
        "keywords": ["game", "strategy"],
        "explanation": "Game strategy context without an explicit harmful action.",
    },

    {
        "pattern": "time management hack",
        "context_type": "benign_optimization",
        "intent": "non-malicious",
        "strength": 0.90,
        "keywords": ["time", "management", "hack"],
        "explanation": "Time-management optimization context.",
    },

    {
        "pattern": "fitness hack",
        "context_type": "benign_optimization",
        "intent": "non-malicious",
        "strength": 0.85,
        "keywords": ["fitness", "hack"],
        "explanation": "Fitness optimization context.",
    },

    {
        "pattern": "learning hack",
        "context_type": "benign_optimization",
        "intent": "non-malicious",
        "strength": 0.90,
        "keywords": ["learning", "hack"],
        "explanation": "Learning optimization context.",
    },


    # --------------------------------------------------------
    # 2. DEFENSIVE SECURITY
    # --------------------------------------------------------

    {
        "pattern": "secure account password",
        "context_type": "defensive_security",
        "intent": "non-malicious",
        "strength": 0.95,
        "keywords": ["secure", "account", "password"],
        "explanation": "Defensive account-security context.",
    },

    {
        "pattern": "secure my password",
        "context_type": "defensive_security",
        "intent": "non-malicious",
        "strength": 0.95,
        "keywords": ["secure", "password"],
        "explanation": "Password protection context.",
    },

    {
        "pattern": "protect my account",
        "context_type": "defensive_security",
        "intent": "non-malicious",
        "strength": 0.95,
        "keywords": ["protect", "account"],
        "explanation": "Defensive account-protection context.",
    },

    {
        "pattern": "protect my password",
        "context_type": "defensive_security",
        "intent": "non-malicious",
        "strength": 0.95,
        "keywords": ["protect", "password"],
        "explanation": "Defensive password-security context.",
    },

    {
        "pattern": "password manager",
        "context_type": "defensive_security",
        "intent": "non-malicious",
        "strength": 0.95,
        "keywords": ["password", "manager"],
        "explanation": "Password-management context.",
    },

    {
        "pattern": "strong password",
        "context_type": "defensive_security",
        "intent": "non-malicious",
        "strength": 0.90,
        "keywords": ["strong", "password"],
        "explanation": "Password-strengthening context.",
    },

    {
        "pattern": "secure login",
        "context_type": "defensive_security",
        "intent": "non-malicious",
        "strength": 0.90,
        "keywords": ["secure", "login"],
        "explanation": "Defensive login-security context.",
    },

    {
        "pattern": "account security",
        "context_type": "defensive_security",
        "intent": "non-malicious",
        "strength": 0.90,
        "keywords": ["account", "security"],
        "explanation": "General defensive account-security context.",
    },

    {
        "pattern": "security best practices",
        "context_type": "defensive_security",
        "intent": "non-malicious",
        "strength": 0.90,
        "keywords": ["security", "best", "practices"],
        "explanation": "Defensive security education context.",
    },

    {
        "pattern": "ethical hacking course",
        "context_type": "defensive_security",
        "intent": "non-malicious",
        "strength": 0.90,
        "keywords": ["ethical", "hacking", "course"],
        "explanation": "Authorized or educational cybersecurity context.",
    },

    {
        "pattern": "penetration testing",
        "context_type": "defensive_security",
        "intent": "non-malicious",
        "strength": 0.80,
        "keywords": ["penetration", "testing"],
        "explanation": "Security-testing context; authorization should still be evaluated downstream.",
    },


    # --------------------------------------------------------
    # 3. SAFE GENERAL CONTEXT
    # --------------------------------------------------------

    {
        "pattern": "how to improve study habits",
        "context_type": "safe_general",
        "intent": "non-malicious",
        "strength": 0.95,
        "keywords": ["improve", "study", "habits"],
        "explanation": "General educational self-improvement context.",
    },

    {
        "pattern": "how to improve productivity",
        "context_type": "safe_general",
        "intent": "non-malicious",
        "strength": 0.90,
        "keywords": ["improve", "productivity"],
        "explanation": "General productivity-improvement context.",
    },

    {
        "pattern": "learn cybersecurity",
        "context_type": "safe_general",
        "intent": "non-malicious",
        "strength": 0.75,
        "keywords": ["learn", "cybersecurity"],
        "explanation": "General cybersecurity learning context.",
    },


    # --------------------------------------------------------
    # 4. AMBIGUOUS LEXICAL CONTEXT
    # --------------------------------------------------------

    {
        "pattern": "hack",
        "context_type": "ambiguous_lexical",
        "intent": "unknown_or_safe",
        "strength": 0.25,
        "keywords": ["hack"],
        "explanation": "The word 'hack' is semantically ambiguous without context.",
    },

    {
        "pattern": "password",
        "context_type": "ambiguous_lexical",
        "intent": "unknown_or_safe",
        "strength": 0.20,
        "keywords": ["password"],
        "explanation": "The word 'password' alone does not establish credential theft.",
    },

    {
        "pattern": "kill",
        "context_type": "ambiguous_lexical",
        "intent": "unknown_or_safe",
        "strength": 0.20,
        "keywords": ["kill"],
        "explanation": "The word 'kill' can have non-human or technical meanings.",
    },
]


# ============================================================
# INDEX
# ============================================================

CONTEXTUAL_SAFETY_INDEX: Dict[str, List[Dict[str, Any]]] = {}

for pattern in CONTEXTUAL_SAFETY_PATTERNS:
    context_type = pattern.get("context_type", "unknown")
    CONTEXTUAL_SAFETY_INDEX.setdefault(
        context_type,
        []
    ).append(pattern)


# ============================================================
# HELPERS
# ============================================================

def _normalize(text: Any) -> str:
    if not isinstance(text, str):
        return ""

    return " ".join(
        text.lower().strip().split()
    )


def _contains_all_keywords(
    text: str,
    keywords: List[str],
) -> bool:

    return all(
        keyword.lower() in text
        for keyword in keywords
    )


# ============================================================
# PATTERN MATCHER
# ============================================================

def match_contextual_safety(
    text: str,
) -> List[Dict[str, Any]]:

    """
    Return contextual safety matches.

    This function does NOT decide the final intent.
    """

    normalized_text = _normalize(text)

    if not normalized_text:
        return []

    matches: List[Dict[str, Any]] = []

    for pattern in CONTEXTUAL_SAFETY_PATTERNS:

        keywords = pattern.get("keywords", [])

        if not keywords:
            continue

        if _contains_all_keywords(
            normalized_text,
            keywords,
        ):
            matches.append(
                {
                    "pattern": pattern["pattern"],
                    "context_type": pattern["context_type"],
                    "intent": pattern["intent"],
                    "strength": float(
                        pattern.get("strength", 0.0)
                    ),
                    "explanation": pattern.get(
                        "explanation",
                        ""
                    ),
                }
            )

    return matches


# ============================================================
# CONTEXT SUMMARY
# ============================================================

def summarize_context(
    text: str,
) -> Dict[str, Any]:

    matches = match_contextual_safety(text)

    if not matches:
        return {
            "matched": False,
            "contexts": [],
            "primary_context": None,
            "context_strength": 0.0,
            "evidence": [],
        }

    contexts = list(
        dict.fromkeys(
            match["context_type"]
            for match in matches
        )
    )

    primary_match = max(
        matches,
        key=lambda item: item.get(
            "strength",
            0.0
        ),
    )

    evidence = [
        {
            "source": "contextual_safety",
            "pattern": match["pattern"],
            "context_type": match["context_type"],
            "intent": match["intent"],
            "strength": round(
                match["strength"],
                3,
            ),
            "explanation": match["explanation"],
        }
        for match in matches
    ]

    return {
        "matched": True,
        "contexts": contexts,
        "primary_context": primary_match[
            "context_type"
        ],
        "context_strength": round(
            primary_match["strength"],
            3,
        ),
        "evidence": evidence,
    }


# ============================================================
# PUBLIC API
# ============================================================

__all__ = [
    "CONTEXTUAL_SAFETY_PATTERNS",
    "CONTEXTUAL_SAFETY_INDEX",
    "match_contextual_safety",
    "summarize_context",
]
