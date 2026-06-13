from backend.core.signal_weights import SIGNAL_WEIGHTS


def calculate_signal_strength(signals):
    """
    Calculate weighted signal strength based on SIGNAL_WEIGHTS.
    Returns normalized score between 0.0 - 1.0
    """

    if not signals or not isinstance(signals, list):
        return 0.0

    total = 0.0

    for s in signals:
        if not s:
            continue
        total += SIGNAL_WEIGHTS.get(s, 0.0)

    normalized = total / (len(signals) + 1)

    return round(max(0.0, min(normalized, 1.0)), 3)
