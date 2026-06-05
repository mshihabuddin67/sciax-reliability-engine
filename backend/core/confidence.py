def calculate_confidence(
    stability,
    behavioral_signals_count=0,
    fuzzy_score=0.0,
    strong_match=False,
    safe_override=False
):

    stability = max(0.0, min(stability, 1.0))

    # ==================================================
    # SAFE OVERRIDE
    # ==================================================
    if safe_override:
        confidence = min(
            0.98,
            0.85 + stability * 0.10
        )
        return round(confidence, 2)

    # ==================================================
    # BASE
    # ==================================================
    confidence = stability * 0.50

    # behavioral evidence
    confidence += min(
        behavioral_signals_count * 0.08,
        0.20
    )

    # fuzzy evidence
    confidence += fuzzy_score * 0.15

    # deterministic keyword hit
    if strong_match:
        confidence += 0.20

    confidence = max(
        0.05,
        min(confidence, 0.99)
    )

    return round(confidence, 2)
