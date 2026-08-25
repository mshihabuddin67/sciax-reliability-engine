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
    S-CIAX Confidence Fusion Engine V4

    Evidence Sources
    ----------------
    • Dynamic Stability
    • Signal Strength
    • Behavioral Signals
    • Fuzzy Match
    • Intent Consistency
    • Evidence Quality
    • Contradiction Score
    • Strong Rule Match
    • Safe Context
    """

    # -----------------------------------------
    # Clamp inputs
    # -----------------------------------------

    stability = max(0.0, min(float(stability), 1.0))
    signal_strength = max(0.0, min(float(signal_strength), 1.0))
    fuzzy_score = max(0.0, min(float(fuzzy_score), 1.0))
    intent_consistency = max(
        0.0,
        min(float(intent_consistency), 1.0)
    )

    evidence_quality = max(
        0.0,
        min(float(evidence_quality), 1.0)
    )

    contradiction_score = max(
        0.0,
        min(float(contradiction_score), 1.0)
    )

    # -----------------------------------------
    # Base Evidence Fusion
    # -----------------------------------------

    raw = 0.0

    raw += stability * 0.25

    raw += signal_strength * 0.20

    raw += min(
        behavioral_signals_count * 0.04,
        0.12
    )

    raw += fuzzy_score * 0.08

    raw += intent_consistency * 0.15

    # -----------------------------------------
    # Evidence Quality
    # -----------------------------------------

    raw += evidence_quality * 0.20

    # -----------------------------------------
    # Contradiction Penalty
    # -----------------------------------------

    raw -= contradiction_score * 0.10

    # -----------------------------------------
    # Strong Match
    # -----------------------------------------

    if strong_match:
        raw += 0.10

    # -----------------------------------------
    # Safe Context
    #
    # Safe context contributes evidence,
    # but does NOT erase contradictory evidence.
    # -----------------------------------------

    if safe_override:

        raw += 0.05

        # Strong contradiction prevents
        # benign context from dominating.
        if contradiction_score >= 0.30:
            raw -= 0.05

    # -----------------------------------------
    # Final Bound
    # -----------------------------------------

    raw = max(0.0, min(raw, 1.0))

    return calibrate_confidence(raw)
