import math


# ==================================================
# 1. CONFIDENCE CALIBRATION
# ==================================================
def calibrate_confidence(raw_score: float) -> float:
    """
    Converts raw heuristic score into a bounded confidence score (0â€“1).
    More stable than a direct sigmoid on small ranges.
    """

    try:
        scaled = raw_score / (1 + abs(raw_score))
        confidence = 1 / (1 + math.exp(-scaled * 3))

        return round(
            max(0.0, min(confidence, 1.0)),
            3
        )

    except Exception:
        return 0.0


# ==================================================
# 2. STABILITY SCORE (RECENT-WEIGHTED)
# ==================================================
def compute_calibrated_stability_score(previous_scores):
    """
    Measures consistency across runs.
    Higher stability = lower variance.
    Recent scores receive slightly higher weight.
    """

    try:

        if not previous_scores:
            return 0.5

        if len(previous_scores) < 2:
            return 1.0

        weights = [
            i / len(previous_scores)
            for i in range(1, len(previous_scores) + 1)
        ]

        weighted_mean = (
            sum(
                score * weight
                for score, weight in zip(
                    previous_scores,
                    weights
                )
            )
            / sum(weights)
        )

        variance = (
            sum(
                (score - weighted_mean) ** 2
                for score in previous_scores
            )
            / len(previous_scores)
        )

        stability = 1 / (1 + variance)

        return round(
            max(0.0, min(stability, 1.0)),
            3
        )

    except Exception:
        return 0.5


# ==================================================
# 3. UNCERTAINTY SCORE
# ==================================================
def compute_uncertainty(
    signals,
    confidence
):
    """
    Estimates uncertainty from:
    - confidence gap
    - signal diversity
    """

    try:

        if not signals:
            return 1.0

        unique_ratio = (
            len(set(signals))
            / max(len(signals), 1)
        )

        confidence_gap = 1 - confidence

        uncertainty = (
            confidence_gap * 0.70
            + (1 - unique_ratio) * 0.30
        )

        return round(
            max(0.0, min(uncertainty, 1.0)),
            3
        )

    except Exception:
        return 1.0
