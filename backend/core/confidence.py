def calculate_confidence(
    stability,
    behavioral_signals_count=0,
    fuzzy_score=0.0,
    strong_match=False,
    safe_override=False
):

    # normalize stability
    stability = max(0.0, min(stability, 1.0))

    # ==================================================
    # SAFE OVERRIDE
    # ==================================================
    if safe_override:
        confidence = min(0.95, 0.85 + stability * 0.1)
        return round(confidence, 2)

    # ==================================================
    # BASE
    # ==================================================
    confidence = 0.30

    confidence += stability * 0.25

    # safer penalty cap
    confidence -= min(0.25, behavioral_signals_count * 0.06)

    confidence += fuzzy_score * 0.20

    if strong_match:
        confidence += 0.20

    confidence = max(0.05, min(confidence, 0.98))

    return round(confidence, 2)
