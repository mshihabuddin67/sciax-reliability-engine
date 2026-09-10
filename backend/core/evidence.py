"""
S-CIAX Evidence Engine V2

Purpose:
    Convert signals, candidate intents, explainability output, and
    contextual-safety analysis into structured evidence.

Design principles:
    - Evidence does NOT make the final risk decision.
    - Context is evidence, not an automatic safety override.
    - Contextual safety is delegated to contextual_safety.py.
    - Derived evidence sources are explicitly marked.
    - Existing analyze_evidence() interface remains compatible.
"""

from __future__ import annotations

from typing import Any, Dict, Iterable, List

from backend.patterns.registry import PATTERN_REGISTRY


# ============================================================
# INTENT ↔ SIGNAL RELATIONSHIP
# ============================================================

INTENT_SIGNAL_MAP = {
    "violent_threat": {
        "violent aggression": 1.00,
        "target-directed aggression": 0.90,
        "implicit threat escalation": 0.90,
        "first-person threat language": 0.85,
    },

    "cyber_intrusion": {
        "cyber intrusion intent": 1.00,
    },

    "fraud": {
        "fraud intent": 1.00,
    },

    "social_engineering": {
        "social engineering": 1.00,
    },

    "credential_theft": {
        "credential theft": 1.00,
    },

    "harassment": {
        "harassment": 0.90,
    },

    "coercion": {
        "coercion": 0.90,
    },

    "non-malicious": {
        "benign optimization context": 0.90,
    },
}


# ============================================================
# SOURCE RELIABILITY
# ============================================================

SOURCE_RELIABILITY = {
    "behavioral_signal": 0.80,
    "intent_engine": 0.75,

    # Explainability is derived from other engine components,
    # therefore it must not be treated as independent evidence.
    "explainability": 0.70,

    # Contextual safety is useful but should not overpower
    # direct harmful behavioral evidence.
    "context": 0.65,
}


# ============================================================
# HELPERS
# ============================================================

def _clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, float(value)))


def _safe_list(value: Any) -> List[Any]:
    if value is None:
        return []

    if isinstance(value, (list, tuple, set)):
        return list(value)

    return [value]


def _normalize(value: Any) -> str:
    if value is None:
        return ""

    return " ".join(str(value).lower().strip().split())


def _make_evidence(
    *,
    intent: str,
    evidence_type: str,
    source: str,
    signal: str,
    strength: float,
    reliability: float,
    relevance: float,
    explanation: str = "",
    independent: bool = True,
) -> Dict[str, Any]:
    """
    Create one normalized evidence item.

    quality intentionally remains compatible with V1:
        strength * 0.50
        + reliability * 0.25
        + relevance * 0.25
    """

    strength = _clamp(strength)
    reliability = _clamp(reliability)
    relevance = _clamp(relevance)

    quality = (
        strength * 0.50
        + reliability * 0.25
        + relevance * 0.25
    )

    return {
        "intent": intent,
        "evidence_type": evidence_type,
        "source": source,
        "signal": signal,
        "strength": round(strength, 4),
        "reliability": round(reliability, 4),
        "relevance": round(relevance, 4),
        "quality": round(_clamp(quality), 4),
        "independent": independent,
        "explanation": explanation,
    }


# ============================================================
# BEHAVIORAL SIGNAL EVIDENCE
# ============================================================

def _extract_signal_evidence(
    signals: Iterable[Any],
    intents: Iterable[Any],
) -> List[Dict[str, Any]]:
    evidence: List[Dict[str, Any]] = []

    signal_list = [
        _normalize(signal)
        for signal in _safe_list(signals)
        if _normalize(signal)
    ]

    intent_list = [
        _normalize(intent)
        for intent in _safe_list(intents)
        if _normalize(intent)
    ]

    for intent in intent_list:
        mapping = INTENT_SIGNAL_MAP.get(intent, {})

        for signal, strength in mapping.items():
            signal_normalized = _normalize(signal)

            if signal_normalized in signal_list:
                evidence.append(
                    _make_evidence(
                        intent=intent,
                        evidence_type="behavioral_signal",
                        source="behavioral_signal",
                        signal=signal,
                        strength=strength,
                        reliability=SOURCE_RELIABILITY["behavioral_signal"],
                        relevance=strength,
                        explanation=(
                            f"Behavioral signal '{signal}' supports "
                            f"intent '{intent}'."
                        ),
                        independent=True,
                    )
                )

    return evidence


# ============================================================
# CANDIDATE INTENT EVIDENCE
# ============================================================

def _extract_intent_evidence(
    intents: Iterable[Any],
) -> List[Dict[str, Any]]:
    evidence: List[Dict[str, Any]] = []

    for intent in _safe_list(intents):
        intent_normalized = _normalize(intent)

        if not intent_normalized:
            continue

        if intent_normalized in {
            "unknown_or_safe",
            "unknown",
        }:
            continue

        evidence.append(
            _make_evidence(
                intent=intent_normalized,
                evidence_type="candidate_intent",
                source="intent_engine",
                signal=intent_normalized,
                strength=0.70,
                reliability=SOURCE_RELIABILITY["intent_engine"],
                relevance=0.90,
                explanation=(
                    f"Intent engine classified candidate intent "
                    f"'{intent_normalized}'."
                ),
                # Candidate intent is derived from the intent engine,
                # not independent ground truth.
                independent=False,
            )
        )

    return evidence


# ============================================================
# EXPLAINABILITY EVIDENCE
# ============================================================

def _extract_explainability_evidence(
    explanations: Iterable[Any],
) -> List[Dict[str, Any]]:
    """
    Preserve V1 explainability evidence behavior.

    IMPORTANT:
        This source is marked independent=False because explanations
        are generally derived from the same underlying detection logic.
    """

    evidence: List[Dict[str, Any]] = []

    keyword_map = {
        "violent_threat": [
            "violent",
            "threat",
            "aggression",
        ],
        "cyber_intrusion": [
            "cyber",
            "intrusion",
            "hack",
            "breach",
            "exploit",
        ],
        "fraud": [
            "fraud",
            "otp",
            "financial",
        ],
        "social_engineering": [
            "social engineering",
            "impersonation",
        ],
        "credential_theft": [
            "credential",
            "password",
            "login",
        ],
        "harassment": [
            "harassment",
            "abusive",
        ],
        "coercion": [
            "coercion",
            "force",
        ],
        "non-malicious": [
            "safe",
            "benign",
            "non-malicious",
        ],
    }

    for explanation in _safe_list(explanations):
        text = _normalize(explanation)

        if not text:
            continue

        for intent, keywords in keyword_map.items():
            matched_keyword = next(
                (
                    keyword
                    for keyword in keywords
                    if keyword in text
                ),
                None,
            )

            if matched_keyword:
                evidence.append(
                    _make_evidence(
                        intent=intent,
                        evidence_type="explainability",
                        source="explainability",
                        signal=matched_keyword,
                        strength=0.65,
                        reliability=SOURCE_RELIABILITY["explainability"],
                        relevance=0.85,
                        explanation=str(explanation),
                        independent=False,
                    )
                )

    return evidence 

# ============================================================
# CONTEXTUAL SAFETY EVIDENCE
# ============================================================

def _extract_context_evidence(
    text: str,
    intents: Iterable[Any],
) -> List[Dict[str, Any]]:
    """
    Extract contextual-safety evidence from the centralized
    Pattern Registry.

    Context is evidence only.
    It does NOT make the final risk decision.

    Contextual patterns can provide independent evidence even
    when the Intent Engine did not initially classify the same
    intent.
    """

    evidence: List[Dict[str, Any]] = []

    if not isinstance(text, str):
        return evidence

    normalized_text = _normalize(text)

    if not normalized_text:
        return evidence

    intent_list = [
        _normalize(intent)
        for intent in _safe_list(intents)
        if _normalize(intent)
    ]

    contextual_patterns = PATTERN_REGISTRY.get(
        "contextual_safety",
        []
    )

    for match in contextual_patterns:

        if not isinstance(match, dict):
            continue

        pattern = _normalize(
            match.get("pattern", "")
        )

        context_type = _normalize(
            match.get("context_type", "")
        )

        context_intent = _normalize(
            match.get(
                "intent",
                "unknown_or_safe",
            )
        )

        strength = _clamp(
            match.get("strength", 0.0)
        )

        explanation = str(
            match.get("explanation", "")
        ).strip()

        if not pattern:
            continue

        # ----------------------------------------------------
        # Pattern match
        # ----------------------------------------------------

        matched = pattern in normalized_text

        # ----------------------------------------------------
        # Structured keyword fallback
        # ----------------------------------------------------

        if not matched:

            keywords = match.get(
                "keywords",
                []
            )

            if isinstance(
                keywords,
                (list, tuple, set),
            ):

                normalized_keywords = [
                    _normalize(keyword)
                    for keyword in keywords
                    if _normalize(keyword)
                ]

                if normalized_keywords:
                    matched = all(
                        keyword in normalized_text
                        for keyword in normalized_keywords
                    )

        if not matched:
            continue

        # ----------------------------------------------------
        # Contextual support
        #
        # IMPORTANT:
        # Do NOT require context_intent to already exist
        # inside intent_list.
        #
        # Example:
        # "secure account password"
        #
        # Intent Engine:
        #     credential_theft
        #
        # Context Engine:
        #     non-malicious
        #
        # Both must reach the Evidence layer.
        # ----------------------------------------------------

        evidence.append(
            _make_evidence(
                intent=context_intent,
                evidence_type="contextual_support",
                source="context",
                signal=pattern,
                strength=strength,
                reliability=SOURCE_RELIABILITY["context"],
                relevance=strength,
                explanation=(
                    explanation
                    or
                    f"Context '{context_type}' supports "
                    f"intent '{context_intent}'."
                ),
                independent=True,
            )
        )

        # ----------------------------------------------------
        # Benign context vs harmful intent
        #
        # Context conflict is intentionally weak.
        # It must NOT erase direct harmful evidence.
        # ----------------------------------------------------

        if context_intent == "non-malicious":

            harmful_intents = [
                intent
                for intent in intent_list
                if intent not in {
                    "non-malicious",
                    "unknown_or_safe",
                    "unknown",
                }
            ]

            for harmful_intent in harmful_intents:

                evidence.append(
                    _make_evidence(
                        intent=harmful_intent,
                        evidence_type="contextual_conflict",
                        source="context",
                        signal=pattern,
                        strength=min(
                            0.25,
                            strength,
                        ),
                        reliability=SOURCE_RELIABILITY["context"],
                        relevance=0.45,
                        explanation=(
                            f"Benign contextual pattern "
                            f"'{pattern}' conflicts with "
                            f"detected intent "
                            f"'{harmful_intent}'."
                        ),
                        independent=True,
                    )
                )

    return evidence

# ============================================================
# CONTRADICTION ANALYSIS
# ============================================================

def compute_contradiction_score(
    evidence: Iterable[Dict[str, Any]],
) -> float:
    """
    Estimate how strongly contextual/semantic evidence conflicts
    with the currently detected evidence.

    Only contextual_conflict items contribute to conflict.

    This prevents ordinary supporting evidence from artificially
    increasing contradiction.
    """

    supportive_quality = 0.0
    conflicting_quality = 0.0

    for item in _safe_list(evidence):
        if not isinstance(item, dict):
            continue

        quality = _clamp(
            item.get("quality", 0.0)
        )

        if item.get("evidence_type") == "contextual_conflict":
            conflicting_quality += quality
        else:
            supportive_quality += quality

    if supportive_quality <= 0:
        return round(_clamp(conflicting_quality), 4)

    score = conflicting_quality / (
        supportive_quality + conflicting_quality
    )

    return round(_clamp(score), 4)


# ============================================================
# EVIDENCE AGGREGATION
# ============================================================

def aggregate_evidence_by_intent(
    evidence: Iterable[Dict[str, Any]],
) -> Dict[str, Dict[str, Any]]:
    """
    Aggregate evidence per intent using diminishing returns.

    Multiple evidence items reinforce confidence without allowing
    simple signal-count inflation.
    """

    grouped: Dict[str, List[Dict[str, Any]]] = {}

    for item in _safe_list(evidence):
        if not isinstance(item, dict):
            continue

        intent = _normalize(
            item.get("intent")
        )

        if not intent:
            continue

        grouped.setdefault(intent, []).append(item)

    result: Dict[str, Dict[str, Any]] = {}

    for intent, items in grouped.items():
        qualities = [
            _clamp(item.get("quality", 0.0))
            for item in items
        ]

        combined = 1.0

        for quality in qualities:
            combined *= (1.0 - quality)

        evidence_score = 1.0 - combined

        average_quality = (
            sum(qualities) / len(qualities)
            if qualities
            else 0.0
        )

        result[intent] = {
            "evidence_score": round(
                _clamp(evidence_score), 4
            ),
            "evidence_count": len(items),
            "average_quality": round(
                _clamp(average_quality), 4
            ),
        }

    return result


# ============================================================
# GLOBAL EVIDENCE QUALITY
# ============================================================

def _compute_global_evidence_quality(
    evidence: Iterable[Dict[str, Any]],
) -> float:
    """
    Calculate global evidence quality while reducing the effect
    of non-independent evidence.

    Independent evidence receives full weight.
    Derived evidence receives a reduced contribution.
    """

    weighted_values = []

    for item in _safe_list(evidence):
        if not isinstance(item, dict):
            continue

        quality = _clamp(
            item.get("quality", 0.0)
        )

        independent = bool(
            item.get("independent", True)
        )

        # Derived evidence should not count as a second
        # independent confirmation of the same decision.
        multiplier = 1.0 if independent else 0.60

        weighted_values.append(
            quality * multiplier
        )

    if not weighted_values:
        return 0.0

    return round(
        _clamp(
            sum(weighted_values)
            / len(weighted_values)
        ),
        4,
    )


# ============================================================
# MAIN EVIDENCE ANALYSIS
# ============================================================

def analyze_evidence(
    text: str,
    signals: Iterable[Any],
    intents: Iterable[Any],
    explanations: Iterable[Any],
) -> Dict[str, Any]:
    """
    Main public Evidence V2 API.

    Existing callers can continue using:
        analyze_evidence(
            text,
            signals,
            intents,
            explanations,
        )
    """

    evidence: List[Dict[str, Any]] = []

    # --------------------------------------------------------
    # 1. Behavioral evidence
    # --------------------------------------------------------

    evidence.extend(
        _extract_signal_evidence(
            signals,
            intents,
        )
    )

    # --------------------------------------------------------
    # 2. Candidate intent evidence
    # --------------------------------------------------------

    evidence.extend(
        _extract_intent_evidence(
            intents
        )
    )

    # --------------------------------------------------------
    # 3. Explainability evidence
    # --------------------------------------------------------

    evidence.extend(
        _extract_explainability_evidence(
            explanations
        )
    )

    # --------------------------------------------------------
    # 4. Contextual safety evidence
    # --------------------------------------------------------

    evidence.extend(
        _extract_context_evidence(
            text,
            intents,
        )
    )

    # --------------------------------------------------------
    # 5. Aggregate
    # --------------------------------------------------------

    intent_evidence = aggregate_evidence_by_intent(
        evidence
    )

    # --------------------------------------------------------
    # 6. Select strongest evidence-supported intent
    # --------------------------------------------------------

    selected_intent = "unknown_or_safe"
    selected_intent_score = 0.0

    for intent, data in intent_evidence.items():
        score = _clamp(
            data.get("evidence_score", 0.0)
        )

        if score > selected_intent_score:
            selected_intent = intent
            selected_intent_score = score

    # --------------------------------------------------------
    # 7. Global evidence quality
    # --------------------------------------------------------

    global_evidence_quality = (
        _compute_global_evidence_quality(
            evidence
        )
    )

    # --------------------------------------------------------
    # 8. Contradiction
    # --------------------------------------------------------

    contradiction_score = compute_contradiction_score(
        evidence
    )

    return {
        "evidence": evidence,
        "intent_evidence": intent_evidence,
        "selected_intent": selected_intent,
        "selected_intent_score": round(
            _clamp(selected_intent_score),
            4,
        ),
        "global_evidence_quality": global_evidence_quality,
        "contradiction_score": contradiction_score,
        "evidence_count": len(evidence),
}
