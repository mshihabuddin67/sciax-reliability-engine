# ==================================================
# S-CIAX RISK FUSION ENGINE V1
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


def compute_final_risk(
    intents,
    signal_strength,
    confidence,
    stability,
    intent_consistency,
    safe_detected=False,
):
    """
    S-CIAX Risk Fusion Engine V1
    """

    if not intents:
        intents = ["unknown_or_safe"]

    severity = max(
        INTENT_SEVERITY.get(intent, 0.0)
        for intent in intents
    )

    risk_score = (
        (severity * 0.35)
        + (signal_strength * 0.25)
        + (confidence * 0.20)
        + (intent_consistency * 0.10)
        + ((1 - stability) * 0.10)
    )

    risk_score = max(0.0, min(risk_score, 1.0))
    risk_score = round(risk_score, 3)

    if risk_score >= 0.85:
        risk_level = "Critical"

    elif risk_score >= 0.65:
        risk_level = "High"

    elif risk_score >= 0.40:
        risk_level = "Medium"

    else:
        risk_level = "Low"

    return {
        "risk_score": risk_score,
        "risk_level": risk_level,
  }
