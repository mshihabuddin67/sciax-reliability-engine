def calculate_uncertainty(
    confidence: float,
    signal_conflict: float = 0.0,
    language_ambiguity: float = 0.0,
    model_disagreement: float = 0.0
):

    confidence = max(0.0, min(confidence, 1.0))

    base_uncertainty = 1 - confidence

    # weighted uncertainty expansion
    extra = (
        signal_conflict * 0.35 +
        language_ambiguity * 0.30 +
        model_disagreement * 0.35
    )

    uncertainty = base_uncertainty + extra

    return round(min(uncertainty, 1.0), 2)
