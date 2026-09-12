# backend/core/semantic_action.py

"""
S-CIAX Semantic Action Evidence Layer

Purpose
-------
Extract lightweight semantic action/object/ownership evidence
without making the final intent or risk decision.

This module is deliberately conservative.

It does NOT:
    - assign final risk level
    - assign final intent
    - override contextual safety
    - replace the existing intent engine

It produces structured semantic evidence that can later be
consumed by evidence.py / intent adjudication.
"""

import re
from typing import Dict, List, Any


# ============================================================
# ACTION GROUPS
# ============================================================

ACTION_PATTERNS = {
    "steal": [
        r"\bsteal\b",
        r"\bstealing\b",
        r"\bstole\b",
        r"\bchuri\b",
        r"\bchuri\s+korbo\b",
        r"\bniye\s+nibo\b",
    ],

    "obtain": [
        r"\bget\b",
        r"\bobtain\b",
        r"\bacquire\b",
        r"\bcollect\b",
        r"\bniye\s+nibo\b",
        r"\bniye\s+nibo\b",
        r"\bber\s+korbo\b",
    ],

    "access": [
        r"\baccess\b",
        r"\baccessing\b",
        r"\benter\b",
        r"\blog\s+into\b",
        r"\blogin\b",
        r"\bdhukbo\b",
        r"\bdhukte\b",
    ],

    "bypass": [
        r"\bbypass\b",
        r"\bget\s+around\b",
        r"\bget\s+past\b",
        r"\bcircumvent\b",
        r"\bavoid\s+(?:the\s+)?login\b",
        r"\bsecurity\s+bypass\b",
        r"\bpas\s+kore\b",
        r"\bumkiye\b",
    ],

    "attack": [
        r"\battack\b",
        r"\btarget\b",
        r"\bhamla\b",
        r"\bacromon\b",
    ],

    "kill": [
        r"\bkill\b",
        r"\bmurder\b",
        r"\bmar\b",
        r"\bmere\b",
        r"\bkhun\b",
        r"\bshesh\s+kore\b",
    ],
}


# ============================================================
# OBJECT GROUPS
# ============================================================

OBJECT_PATTERNS = {
    "password": [
        r"\bpassword\b",
        r"\bpass\b",
        r"\bp@ss\b",
        r"\bp4ss\b",
        r"\bp455\b",
        r"\bpassw(?:o|0)rd\b",
    ],

    "account": [
        r"\baccount\b",
        r"\bacc(?:ount)?\b",
        r"\bacc0unt\b",
        r"\bprofile\b",
    ],

    "login": [
        r"\blogin\b",
        r"\blog\s+in\b",
        r"\bsign\s+in\b",
        r"\bauthentication\b",
        r"\bauth\b",
    ],

    "otp": [
        r"\botp\b",
        r"\bone\s*time\s+password\b",
        r"\bverification\s+code\b",
        r"\bverification\s+otp\b",
    ],

    "credentials": [
        r"\bcredentials\b",
        r"\blogin\s+credentials\b",
        r"\busername\s+and\s+password\b",
    ],

    "data": [
        r"\bdata\b",
        r"\binformation\b",
        r"\bfiles?\b",
        r"\bdatabase\b",
    ],

    "server": [
        r"\bserver\b",
        r"\bhost\b",
        r"\bsystem\b",
        r"\bnetwork\b",
    ],

    "person": [
        r"\byou\b",
        r"\byour\b",
        r"\bhim\b",
        r"\bher\b",
        r"\bthem\b",
        r"\btheir\b",
        r"\bsomeone\b",
        r"\bsomebody\b",
    ],
}


# ============================================================
# OWNERSHIP / TARGET CUES
# ============================================================

THIRD_PARTY_CUES = [
    r"\bsomeone\s+else'?s\b",
    r"\bsomeone\s+else\b",
    r"\bsomebody\s+else'?s\b",
    r"\banother\s+person'?s\b",
    r"\banother\s+user'?s\b",
    r"\btheir\b",
    r"\bhis\b",
    r"\bher\b",
    r"\bthem\b",
    r"\btore\b",
    r"\btomake\b",
    r"\btar\b",
    r"\bonnor\b",
    r"\bonner\b",
]

SELF_CUES = [
    r"\bmy\b",
    r"\bmine\b",
    r"\bmyself\b",
    r"\bamar\b",
    r"\bamar\s+account\b",
    r"\bamar\s+password\b",
]

DIRECT_TARGET_CUES = [
    r"\byou\b",
    r"\byour\b",
    r"\btoke\b",
    r"\btomake\b",
    r"\btore\b",
    r"\btujhe\b",
    r"\btumhe\b",
]


# ============================================================
# AUTHORIZATION CUES
# ============================================================

AUTHORIZATION_CUES = [
    r"\bmy\s+account\b",
    r"\bmy\s+password\b",
    r"\bmy\s+server\b",
    r"\bmy\s+system\b",
    r"\bwith\s+permission\b",
    r"\bauthorized\b",
    r"\bauthorised\b",
    r"\bpermission\b",
    r"\bconsent\b",
    r"\bapproved\b",
]


# ============================================================
# NEGATION CUES
# ============================================================

NEGATION_CUES = [
    r"\bnot\b",
    r"\bnever\b",
    r"\bno\b",
    r"\bdon'?t\b",
    r"\bdo\s+not\b",
    r"\bwon'?t\b",
    r"\bwouldn'?t\b",
    r"\bcan't\b",
    r"\bcannot\b",
    r"\bna\b",
    r"\bnei\b",
    r"\bnoy\b",
    r"\bnai\b",
]


# ============================================================
# NORMALIZATION
# ============================================================

def _normalize(text: str) -> str:
    """
    Lightweight normalization only.

    Important:
    This intentionally does NOT perform aggressive semantic rewriting.
    Existing S-CIAX normalization remains the primary normalization layer.
    """

    if not isinstance(text, str):
        return ""

    text = text.lower().strip()

    # Normalize common separators.
    text = re.sub(r"[_/|]+", " ", text)

    # Keep apostrophes because "someone else's" is meaningful.
    text = re.sub(r"\s+", " ", text)

    return text


# ============================================================
# MATCH HELPERS
# ============================================================

def _match_patterns(text: str, patterns: List[str]) -> List[str]:
    matches = []

    for pattern in patterns:
        try:
            if re.search(pattern, text, flags=re.IGNORECASE):
                matches.append(pattern)
        except re.error:
            continue

    return matches


def _first_match_group(
    text: str,
    pattern_groups: Dict[str, List[str]],
) -> List[Dict[str, Any]]:
    """
    Return all matched semantic groups.
    """

    results = []

    for group_name, patterns in pattern_groups.items():
        matches = _match_patterns(text, patterns)

        if matches:
            results.append(
                {
                    "type": group_name,
                    "matched_patterns": matches,
                }
            )

    return results


# ============================================================
# OWNERSHIP
# ============================================================

def _detect_ownership(text: str) -> Dict[str, Any]:

    third_party = _match_patterns(text, THIRD_PARTY_CUES)
    self_owned = _match_patterns(text, SELF_CUES)
    direct_target = _match_patterns(text, DIRECT_TARGET_CUES)

    if third_party:
        ownership = "third_party"
    elif self_owned:
        ownership = "self"
    elif direct_target:
        ownership = "direct_target"
    else:
        ownership = "unknown"

    return {
        "ownership": ownership,
        "third_party": bool(third_party),
        "self_owned": bool(self_owned),
        "direct_target": bool(direct_target),
        "matched_cues": third_party + self_owned + direct_target,
    }


# ============================================================
# AUTHORIZATION
# ============================================================

def _detect_authorization(text: str) -> Dict[str, Any]:

    matches = _match_patterns(text, AUTHORIZATION_CUES)

    if matches:
        status = "explicit_or_contextual"
    else:
        status = "unknown"

    return {
        "status": status,
        "matched_cues": matches,
    }


# ============================================================
# POLARITY
# ============================================================

def _detect_polarity(text: str) -> Dict[str, Any]:

    matches = _match_patterns(text, NEGATION_CUES)

    if not matches:
        return {
            "polarity": "affirmed",
            "negation_detected": False,
            "matched_cues": [],
        }

    return {
        "polarity": "negation_present",
        "negation_detected": True,
        "matched_cues": matches,
    }


# ============================================================
# SEMANTIC RELEVANCE
# ============================================================

def _compute_relevance(
    actions: List[Dict[str, Any]],
    objects: List[Dict[str, Any]],
    ownership: Dict[str, Any],
) -> str:

    action_types = {item["type"] for item in actions}
    object_types = {item["type"] for item in objects}

    high_risk_actions = {
        "steal",
        "bypass",
        "access",
        "attack",
        "kill",
    }

    sensitive_objects = {
        "password",
        "account",
        "login",
        "otp",
        "credentials",
        "data",
        "server",
    }

    if (
        action_types.intersection(high_risk_actions)
        and object_types.intersection(sensitive_objects)
        and ownership.get("ownership") == "third_party"
    ):
        return "high"

    if action_types.intersection(high_risk_actions):
        return "elevated"

    if object_types.intersection(sensitive_objects):
        return "context_dependent"

    return "low"


# ============================================================
# ACTION → EVIDENCE TYPE
# ============================================================

def _derive_evidence_type(
    actions: List[Dict[str, Any]],
    objects: List[Dict[str, Any]],
    ownership: Dict[str, Any],
) -> str:

    action_types = {item["type"] for item in actions}
    object_types = {item["type"] for item in objects}

    if (
        "kill" in action_types
        and ownership.get("ownership") == "direct_target"
    ):
        return "violent_action"

    if (
        action_types.intersection({"steal", "obtain"})
        and object_types.intersection(
            {"password", "otp", "credentials", "data"}
        )
        and ownership.get("ownership") == "third_party"
    ):
        return "credential_or_data_acquisition"

    if (
        action_types.intersection({"access", "bypass"})
        and object_types.intersection(
            {"account", "login", "server", "system"}
        )
        and ownership.get("ownership") == "third_party"
    ):
        return "unauthorized_access"

    if "attack" in action_types:
        return "attack_action"

    return "semantic_action"


# ============================================================
# PUBLIC API
# ============================================================

def extract_semantic_action(text: str) -> Dict[str, Any]:
    """
    Extract structured semantic action evidence.

    Returns a stable dictionary so that engine.py can consume it
    without changing the existing API response immediately.
    """

    normalized = _normalize(text)

    if not normalized:
        return {
            "semantic_action_detected": False,
            "actions": [],
            "objects": [],
            "ownership": {
                "ownership": "unknown",
                "third_party": False,
                "self_owned": False,
                "direct_target": False,
                "matched_cues": [],
            },
            "authorization": {
                "status": "unknown",
                "matched_cues": [],
            },
            "polarity": {
                "polarity": "affirmed",
                "negation_detected": False,
                "matched_cues": [],
            },
            "relevance": "low",
            "evidence_type": "semantic_action",
        }

    actions = _first_match_group(normalized, ACTION_PATTERNS)
    objects = _first_match_group(normalized, OBJECT_PATTERNS)

    ownership = _detect_ownership(normalized)
    authorization = _detect_authorization(normalized)
    polarity = _detect_polarity(normalized)

    relevance = _compute_relevance(
        actions=actions,
        objects=objects,
        ownership=ownership,
    )

    evidence_type = _derive_evidence_type(
        actions=actions,
        objects=objects,
        ownership=ownership,
    )

    detected = bool(actions or objects)

    return {
        "semantic_action_detected": detected,
        "actions": actions,
        "objects": objects,
        "ownership": ownership,
        "authorization": authorization,
        "polarity": polarity,
        "relevance": relevance,
        "evidence_type": evidence_type,
    }


# ============================================================
# COMPATIBILITY ALIAS
# ============================================================

def analyze_semantic_action(text: str) -> Dict[str, Any]:
    """
    Compatibility-friendly alias for future engine integration.
    """

    return extract_semantic_action(text)
