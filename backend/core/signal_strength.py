from backend.core.signal_weights import SIGNAL_WEIGHTS


def calculate_signal_strength(signals):
    """
    Calculate weighted signal strength based on predefined SIGNAL_WEIGHTS.
    Returns normalized score between 0.0 - 1.0 (approx).
    """

    if not signals:
        return 0.0

    total = 0.0

    for s in signals:
        total += SIGNAL_WEIGHTS.get(s, 0.0)

    # normalize by signal count (avoid division by zero)
    normalized = total / (len(signals) + 1)

    return round(normalized, 3)
