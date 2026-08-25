from backend.core.sciax_calibration_core import calibrate_confidence


def compute_final_confidence(
    stability,
    signal_strength=0.0,
    behavioral_signals_count=0,
    fuzzy_score=0.0,
    intent_consistency=1.0,
    evidence_quality=0.0,
    contradiction_score=0.0,
    strong_match=False,
    safe_override=False
):
    """
    S-CIAX Confidence Fusion Engine V3

    Evidence Sources
    ----------------
    • Dynamic Stability
    • Signal Strength
    • Behavioral Signals
    • Fuzzy Match
    • Intent Consistency
    • Strong Rule Match
    • Safe Override
    """

    # -----------------------------------------
    # Clamp inputs
    # -----------------------------------------

    stability = max(0.0, min(stability, 1.0))
    signal_strength = max(0.0, min(signal_strength, 1.0))
    fuzzy_score = max(0.0, min(fuzzy_score, 1.0))
    intent_consistency = max(0.0, min(intent_consistency, 1.0))

    # -----------------------------------------
    # Safe Override
    # -----------------------------------------

    if safe_override:

        raw = (
            stability * 0.60 +
            intent_consistency * 0.40
        )

        return calibrate_confidence(raw)

    # -----------------------------------------
    # Base Evidence
    # -----------------------------------------

    raw = 0.0

    raw += stability * 0.35

    raw += signal_strength * 0.25

    raw += min(
        behavioral_signals_count * 0.05,
        0.15
    )

    raw += fuzzy_score * 0.10

    raw += intent_consistency * 0.15

    # -----------------------------------------
    # Strong Match Boost
    # -----------------------------------------

    if strong_match:
        raw += 0.15

    raw = max(0.0, min(raw, 1.20))

    return calibrate_confidence(raw)
