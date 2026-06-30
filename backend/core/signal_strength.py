from backend.core.signal_weights import SIGNAL_WEIGHTS

def calculate_signal_strength(signals):

    if not signals or not isinstance(signals, list):
        return 0.0

    score = 0.0

    for signal in signals:

        weight = SIGNAL_WEIGHTS.get(signal, 0.0)

        score += weight

    # interaction bonus
    if (
        "fraud intent" in signals and
        "social engineering" in signals
    ):
        score += 0.08

    if (
        "cyber intrusion intent" in signals and
        "credential theft" in signals
    ):
        score += 0.10

    score = max(0.0, min(score, 1.0))

    return round(score, 3)
