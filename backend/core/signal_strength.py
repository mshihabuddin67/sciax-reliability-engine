from backend.core.signal_weights import SIGNAL_WEIGHTS

def calculate_signal_strength(signals):

    if not signals:
        return 0.0

    total = 0.0

    for s in signals:
        total += SIGNAL_WEIGHTS.get(s, 0.0)

    # normalize by signal count
    normalized = total / (len(signals) + 1)

    return round(normalized, 3)
