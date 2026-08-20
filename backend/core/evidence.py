"""
S-CIAX Evidence Engine V1

Purpose
-------
Convert detected signals, candidate intents, explainability signals,
and contextual information into structured evidence.

This module does NOT make the final risk decision.
It provides evidence for downstream intent, confidence, and risk fusion.

Architecture:

Signals
   ↓
Evidence Extraction
   ↓
Evidence Quality
   ↓
Intent Support / Contradiction
   ↓
Downstream Reasoning
"""

from typing import Any, Dict, List


# ============================================================
# CONFIGURATION
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


# Evidence source reliability.
# These are deliberately conservative starting values.
SOURCE_RELIABILITY = {
    "behavioral_signal": 0.80,
    "intent_engine": 0.75,
    "explainability": 0.70,
    "context": 0.65,
}


# ============================================================
# HELPERS
# ============================================================

def _clamp(value: float) -> float:
    return max(0.0, min(float(value), 1.0))


def _safe_list(value: Any) -> List:
    if isinstance(value, list):
        return value
    return []


def _normalize(value: Any) -> str:
    if not isinstance(value, str):
        return ""
    return value.strip().lower()


# ============================================================
# EVIDENCE OBJECT
# ============================================================

def _make_evidence(
    *,
    intent: str,
    evidence_type: str,
    source: str,
    strength: float,
    reliability: float,
    relevance: float,
    signal: str | None = None,
    explanation: str | None = None,
) -> Dict[str, Any]:

    strength = _clamp(strength)
    reliability = _clamp(reliability)
    relevance = _clamp(relevance)

    # Evidence quality is NOT simply signal strength.
    # Reliability and contextual relevance also matter.
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
        "strength": round(strength, 3),
        "reliability": round(reliability, 3),
        "relevance": round(relevance, 3),
        "quality": round(_clamp(quality), 3),
        "explanation": explanation,
    }


# ============================================================
# SIGNAL → EVIDENCE
# ============================================================

def _extract_signal_evidence(
    signals: List[str],
    intents: List[str],
) -> List[Dict[str, Any]]:

    evidence = []

    normalized_signals = {
        _normalize(signal)
        for signal in signals
    }

    for intent in intents:

        intent_key = _normalize(intent)

        mappings = INTENT_SIGNAL_MAP.get(intent_key, {})

        for signal, base_strength in mappings.items():

            normalized_signal = _normalize(signal)

            if normalized_signal not in normalized_signals:
                continue

            evidence.append(
                _make_evidence(
                    intent=intent_key,
                    evidence_type="behavioral",
                    source="behavioral_signal",
                    strength=base_strength,
                    reliability=SOURCE_RELIABILITY["behavioral_signal"],
                    relevance=1.0,
                    signal=signal,
                    explanation=(
                        f"Behavioral signal '{signal}' "
                        f"supports intent '{intent_key}'."
                    ),
                )
            )

    return evidence


# ============================================================
# INTENT ENGINE EVIDENCE
# ============================================================

def _extract_intent_evidence(
    intents: List[str],
) -> List[Dict[str, Any]]:

    evidence = []

    for intent in intents:

        intent_key = _normalize(intent)

        if intent_key == "unknown_or_safe":
            continue

        evidence.append(
            _make_evidence(
                intent=intent_key,
                evidence_type="candidate_intent",
                source="intent_engine",
                strength=0.70,
                reliability=SOURCE_RELIABILITY["intent_engine"],
                relevance=0.90,
                explanation=(
                    f"Intent engine generated '{intent_key}' "
                    "as a candidate interpretation."
                ),
            )
        )

    return evidence


# ============================================================
# EXPLAINABILITY EVIDENCE
# ============================================================

def _extract_explainability_evidence(
    explanations: List[str],
    intents: List[str],
) -> List[Dict[str, Any]]:

    evidence = []

    if not explanations:
        return evidence

    # Explainability should support evidence,
    # but should NOT dominate behavioral evidence.
    for explanation in explanations:

        explanation_text = _normalize(explanation)

        if not explanation_text:
            continue

        matched_intent = None

        if any(
            term in explanation_text
            for term in [
                "violent",
                "aggression",
                "threat",
                "murder",
                "kill",
            ]
        ):
            if "violent_threat" in intents:
                matched_intent = "violent_threat"

        elif "cyber" in explanation_text or "system access" in explanation_text:
            if "cyber_intrusion" in intents:
                matched_intent = "cyber_intrusion"

        elif "credential" in explanation_text:
            if "credential_theft" in intents:
                matched_intent = "credential_theft"

        elif "fraud" in explanation_text:
            if "fraud" in intents:
                matched_intent = "fraud"

        elif "social engineering" in explanation_text:
            if "social_engineering" in intents:
                matched_intent = "social_engineering"

        elif "harassment" in explanation_text:
            if "harassment" in intents:
                matched_intent = "harassment"

        elif "coerc" in explanation_text:
            if "coercion" in intents:
                matched_intent = "coercion"

        elif "safe context" in explanation_text:
            if "non-malicious" in intents:
                matched_intent = "non-malicious"

        if matched_intent:

            evidence.append(
                _make_evidence(
                    intent=matched_intent,
                    evidence_type="explainability",
                    source="explainability",
                    strength=0.65,
                    reliability=SOURCE_RELIABILITY["explainability"],
                    relevance=0.85,
                    explanation=explanation,
                )
            )

    return evidence


# ============================================================
# CONTEXT EVIDENCE
# ============================================================

def _extract_context_evidence(
    text: str,
    intents: List[str],
) -> List[Dict[str, Any]]:

    evidence = []

    text = _normalize(text)

    benign_markers = [
        "sleep schedule",
        "study hack",
        "life hack",
        "productivity hack",
        "game strategy",
    ]

    has_benign_context = any(
        marker in text
        for marker in benign_markers
    )

    if has_benign_context:

        if "non-malicious" in intents:

            evidence.append(
                _make_evidence(
                    intent="non-malicious",
                    evidence_type="context",
                    source="context",
                    strength=0.85,
                    reliability=SOURCE_RELIABILITY["context"],
                    relevance=0.90,
                    explanation="Benign contextual marker detected.",
                )
            )

        # If high-risk intent also exists, the benign context
        # becomes contextual evidence rather than an override.
        for risky_intent in intents:

            if risky_intent in {
                "violent_threat",
                "cyber_intrusion",
                "fraud",
                "credential_theft",
                "social_engineering",
                "harassment",
                "coercion",
            }:

                evidence.append(
                    _make_evidence(
                        intent=risky_intent,
                        evidence_type="contextual_conflict",
                        source="context",
                        strength=0.25,
                        reliability=SOURCE_RELIABILITY["context"],
                        relevance=0.45,
                        explanation=(
                            "Benign context coexists with "
                            f"high-risk intent '{risky_intent}'."
                        ),
                    )
                )

    return evidence


# ============================================================
# CONTRADICTION ANALYSIS
# ============================================================

def compute_contradiction_score(
    evidence: List[Dict[str, Any]],
) -> float:

    if not evidence:
        return 0.0

    supportive = [
        item
        for item in evidence
        if item.get("evidence_type")
        != "contextual_conflict"
    ]

    conflicting = [
        item
        for item in evidence
        if item.get("evidence_type")
        == "contextual_conflict"
    ]

    if not supportive:
        return 0.0

    conflict_strength = sum(
        item.get("quality", 0.0)
        for item in conflicting
    )

    support_strength = sum(
        item.get("quality", 0.0)
        for item in supportive
    )

    if support_strength <= 0:
        return 1.0

    return round(
        _clamp(conflict_strength / support_strength),
        3,
    )


# ============================================================
# INTENT EVIDENCE AGGREGATION
# ============================================================

def aggregate_evidence_by_intent(
    evidence: List[Dict[str, Any]],
) -> Dict[str, Dict[str, float]]:

    grouped: Dict[str, List[Dict[str, Any]]] = {}

    for item in evidence:

        intent = item.get("intent")

        if not intent:
            continue

        grouped.setdefault(intent, []).append(item)

    result = {}

    for intent, items in grouped.items():

        qualities = [
            _clamp(item.get("quality", 0.0))
            for item in items
        ]

        if not qualities:
            continue

        # Diminishing-return aggregation.
        # Prevents 10 duplicate signals from creating
        # artificially perfect evidence.
        combined = 1.0

        for quality in qualities:
            combined *= (1.0 - quality)

        combined = 1.0 - combined

        result[intent] = {
            "evidence_score": round(
                _clamp(combined),
                3,
            ),
            "evidence_count": len(items),
            "average_quality": round(
                sum(qualities) / len(qualities),
                3,
            ),
        }

    return result


# ============================================================
# MAIN EVIDENCE ENGINE
# ============================================================

def analyze_evidence(
    text: str,
    signals: List[str] | None = None,
    intents: List[str] | None = None,
    explanations: List[str] | None = None,
) -> Dict[str, Any]:

    if not isinstance(text, str):
        text = ""

    signals = _safe_list(signals)
    intents = _safe_list(intents)
    explanations = _safe_list(explanations)

    evidence = []

    # --------------------------------------------------------
    # 1. Behavioral Evidence
    # --------------------------------------------------------

    evidence.extend(
        _extract_signal_evidence(
            signals=signals,
            intents=intents,
        )
    )

    # --------------------------------------------------------
    # 2. Candidate Intent Evidence
    # --------------------------------------------------------

    evidence.extend(
        _extract_intent_evidence(
            intents=intents,
        )
    )

    # --------------------------------------------------------
    # 3. Explainability Evidence
    # --------------------------------------------------------

    evidence.extend(
        _extract_explainability_evidence(
            explanations=explanations,
            intents=intents,
        )
    )

    # --------------------------------------------------------
    # 4. Context Evidence
    # --------------------------------------------------------

    evidence.extend(
        _extract_context_evidence(
            text=text,
            intents=intents,
        )
    )

    # --------------------------------------------------------
    # 5. Aggregate
    # --------------------------------------------------------

    intent_evidence = aggregate_evidence_by_intent(
        evidence
    )

    contradiction_score = compute_contradiction_score(
        evidence
    )

    # --------------------------------------------------------
    # 6. Best Supported Intent
    # --------------------------------------------------------

    selected_intent = None
    selected_score = 0.0

    for intent, data in intent_evidence.items():

        score = data["evidence_score"]

        if score > selected_score:
            selected_intent = intent
            selected_score = score

    # --------------------------------------------------------
    # 7. Global Evidence Quality
    # --------------------------------------------------------

    if evidence:

        global_quality = sum(
            item.get("quality", 0.0)
            for item in evidence
        ) / len(evidence)

    else:
        global_quality = 0.0

    return {
        "evidence": evidence,
        "intent_evidence": intent_evidence,
        "selected_intent": selected_intent,
        "selected_intent_score": round(
            _clamp(selected_score),
            3,
        ),
        "global_evidence_quality": round(
            _clamp(global_quality),
            3,
        ),
        "contradiction_score": contradiction_score,
        "evidence_count": len(evidence),
  }
