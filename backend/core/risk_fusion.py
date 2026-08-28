# ==================================================
# S-CIAX RISK FUSION ENGINE V3
# Evidence-Aware + Backward Compatible
# ==================================================

INTENT_SEVERITY = {
    "unknown_or_safe": 0.00,
    "non-malicious": 0.00,
    "harassment": 0.45,
    "coercion": 0.55,
    "social_engineering": 0.65,
    "credential_theft": 0.70,
    "fraud": 0.75,
    "cyber_intrusion": 0.85,
    "violent_threat": 1.00,
}


HIGH_RISK_INTENTS = {
    "violent_threat",
    "cyber_intrusion",
    "fraud",
    "credential_theft",
    "social_engineering",
}


# ==================================================
# HELPERS
# ==================================================

def _clamp(value):
    return max(0.0, min(float(value), 1.0))


# ==================================================
# MAIN RISK FUSION
# ==================================================

def compute_final_risk(
    intents,
    signal_strength,
    confidence,
    stability,
    intent_consistency,
    safe_detected=False,
    evidence_quality=0.0,
    contradiction_score=0.0,
):
    """
    S-CIAX Risk Fusion Engine V3

    Core Foundation Preserved
    -------------------------
    • Intent severity remains dominant.
    • High-risk safety floor remains.
    • Existing risk thresholds remain.
    • Stability remains a secondary factor.
    • Safe context remains bounded.

    New Evidence-Aware Layer
    -------------------------
    • evidence_quality
    • contradiction_score

    Important:
        Evidence and contradiction are bounded adjustments.
        They do NOT replace semantic severity.
    """

    # --------------------------------------------------
    # Input normalization
    # --------------------------------------------------

    if not intents:
        intents = ["unknown_or_safe"]

    signal_strength = _clamp(signal_strength)
    confidence = _clamp(confidence)
    stability = _clamp(stability)
    intent_consistency = _clamp(intent_consistency)

    evidence_quality = _clamp(evidence_quality)
    contradiction_score = _clamp(contradiction_score)

    # --------------------------------------------------
    # Intent Severity
    # --------------------------------------------------

    severity = max(
        INTENT_SEVERITY.get(
            intent,
            0.0
        )
        for intent in intents
    )

    # --------------------------------------------------
    # EXISTING RISK FOUNDATION
    # --------------------------------------------------

    base_risk_score = (
        (severity * 0.50)
        + (signal_strength * 0.20)
        + (confidence * 0.15)
        + (intent_consistency * 0.10)
        + ((1.0 - stability) * 0.05)
    )

    # --------------------------------------------------
    # EVIDENCE QUALITY ADJUSTMENT
    # --------------------------------------------------
    #
    # Evidence quality should improve confidence in
    # an already-supported interpretation.
    #
    # It must NOT independently create high risk.
    #
    # Maximum contribution: +0.05
    #

    evidence_adjustment = (
        evidence_quality * 0.05
    )

    # --------------------------------------------------
    # CONTRADICTION ADJUSTMENT
    # --------------------------------------------------
    #
    # Contradiction represents competing evidence.
    #
    # It should reduce certainty of the risk estimate,
    # but must NOT erase strong high-risk evidence.
    #
    # Maximum reduction: -0.05
    #

    contradiction_adjustment = (
        contradiction_score * 0.05
    )

    # --------------------------------------------------
    # Apply Evidence Layer
    # --------------------------------------------------

    risk_score = (
        base_risk_score
        + evidence_adjustment
        - contradiction_adjustment
    )

    # --------------------------------------------------
    # Safe Context
    # --------------------------------------------------
    #
    # Preserve existing bounded safe-context behavior.
    #
    # Safe context cannot override strong high-risk
    # semantic evidence because the high-risk floor
    # is applied afterward.
    #

    if safe_detected:
        risk_score *= 0.60

    risk_score = _clamp(risk_score)

    # --------------------------------------------------
    # HIGH-RISK SAFETY FLOOR
    # --------------------------------------------------
    #
    # This is intentionally preserved from V2.
    #
    # A benign context or contradiction signal cannot
    # collapse a genuine high-risk intent to Low.
    #

    has_high_risk_intent = any(
        intent in HIGH_RISK_INTENTS
        for intent in intents
    )

    if has_high_risk_intent:
        risk_score = max(
            risk_score,
            0.65
        )

    # --------------------------------------------------
    # Risk Levels
    # --------------------------------------------------

    if risk_score >= 0.85:
        risk_level = "Critical"

    elif risk_score >= 0.65:
        risk_level = "High"

    elif risk_score >= 0.40:
        risk_level = "Medium"

    else:
        risk_level = "Low"

    # --------------------------------------------------
    # Risk Quality
    # --------------------------------------------------

    if (
        confidence >= 0.85
        and evidence_quality >= 0.75
        and contradiction_score <= 0.20
    ):
        risk_quality = "high_certainty"

    elif contradiction_score >= 0.50:
        risk_quality = "ambiguous"

    else:
        risk_quality = "standard"

    # --------------------------------------------------
    # Return
    # --------------------------------------------------

    return {
        "risk_score": round(
            risk_score,
            3
        ),

        "risk_level": risk_level,

        "risk_quality": risk_quality,

        "evidence_quality": round(
            evidence_quality,
            3
        ),

        "contradiction_score": round(
            contradiction_score,
            3
        ),

        "severity_score": round(
            severity,
            3
        ),
    }
