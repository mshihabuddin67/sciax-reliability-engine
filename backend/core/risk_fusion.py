# ==================================================
# S-CIAX RISK FUSION ENGINE V2
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


def compute_final_risk(
    intents,
    signal_strength,
    confidence,
    stability,
    intent_consistency,
    safe_detected=False,
):

    if not intents:
        intents = ["unknown_or_safe"]

    severity = max(
        INTENT_SEVERITY.get(intent, 0.0)
        for intent in intents
    )

    # -----------------------------
    # Risk Fusion
    # -----------------------------

    risk_score = (
        (severity * 0.50)
        + (signal_strength * 0.20)
        + (confidence * 0.15)
        + (intent_consistency * 0.10)
        + ((1 - stability) * 0.05)
    )

    # -----------------------------
    # Safe Context
    # -----------------------------

    if safe_detected:
        risk_score *= 0.60

    risk_score = max(0.0, min(risk_score, 1.0))
    risk_score = round(risk_score, 3)

    # -----------------------------
    # High-Risk Override
    # -----------------------------

    if any(intent in HIGH_RISK_INTENTS for intent in intents):
        risk_score = max(risk_score, 0.65)

    # -----------------------------
    # Risk Levels
    # -----------------------------

    if risk_score >= 0.85:
        risk_level = "Critical"

    elif risk_score >= 0.65:
        risk_level = "High"

    elif risk_score >= 0.40:
        risk_level = "Medium"

    else:
        risk_level = "Low"

    return {
        "risk_score": round(risk_score, 3),
        "risk_level": risk_level,
    }
