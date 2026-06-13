def calculate_confidence(
    stability,
    behavioral_signals_count=0,
    fuzzy_score=0.0,
    signal_strength=0.0,
    strong_match=False,
    safe_override=False
):

    stability = max(0.0, min(stability, 1.0))
    signal_strength = max(0.0, min(signal_strength, 1.0))

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
    # BASE CONFIDENCE (CORE STABILITY)
    # ==================================================
    confidence = stability * 0.45

    # ==================================================
    # BEHAVIORAL EVIDENCE
    # ==================================================
    confidence += min(
        behavioral_signals_count * 0.06,
        0.18
    )

    # ==================================================
    # FUZZY / SEMANTIC EVIDENCE
    # ==================================================
    confidence += fuzzy_score * 0.12

    # ==================================================
    # SIGNAL STRENGTH INFLUENCE (NEW IMPORTANT LAYER)
    # ==================================================
    confidence += signal_strength * 0.20

    # ==================================================
    # STRONG KEYWORD / RULE HIT BOOST
    # ==================================================
    if strong_match:
        confidence += 0.18

    # ==================================================
    # NON-LINEAR STABILIZATION (IMPORTANT)
    # ==================================================
    if stability > 0.85:
        confidence *= 1.05

    # ==================================================
    # BOUNDING (SAFE RANGE)
    # ==================================================
    confidence = max(0.05, min(confidence, 0.99))

    return round(confidence, 2)
