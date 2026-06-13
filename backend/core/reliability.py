def calculate_reliability(
    stability: float,
    confidence: float,
    uncertainty: float = 0.0,
    signal_strength: float = 0.0
):

    stability = max(0.0, min(stability, 1.0))
    confidence = max(0.0, min(confidence, 1.0))
    uncertainty = max(0.0, min(uncertainty, 1.0))

    base = stability * confidence

    penalty = (
        uncertainty * 0.5 +
        signal_strength * 0.3
    )

    reliability = base - penalty

    return round(
        max(0.0, min(reliability, 1.0)),
        2
    )
