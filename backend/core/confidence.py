# ==================================================
# CONFIDENCE ENGINE
# ==================================================

def calculate_confidence(
    stability,
    behavioral_signals_count=0,
    fuzzy_score=0.0,
    strong_match=False
):
    """
    Dynamic confidence scoring.
    """

    confidence = 0.30

    # stability contribution
    confidence += stability * 0.20

    # behavioral signals contribution
    confidence += (
        behavioral_signals_count * 0.10
    )

    # fuzzy similarity contribution
    confidence += (
        fuzzy_score * 0.20
    )

    # strong match boost
    if strong_match:
        confidence += 0.25

    return calibrate_confidence(
        confidence
    )


def calibrate_confidence(raw_score):
    """
    Normalize confidence score.
    """

    raw_score = min(
        raw_score,
        0.99
    )

    return round(
        raw_score,
        2
    )


def calculate_uncertainty(confidence):
    """
    Uncertainty is inverse confidence.
    """

    return round(
        1 - confidence,
        2
    )
