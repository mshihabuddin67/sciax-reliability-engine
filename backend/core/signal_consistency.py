from backend.core.behavioral_signals import (
    detect_behavioral_signals
)


def compute_signal_consistency(variants):
    """
    Signal Consistency Engine V3

    Measures how consistently behavioral
    signals appear across generated variants.

    Returns:
        float (0.0 - 1.0)
    """

    if not variants:
        return 0.0

    if len(variants) == 1:
        return 1.0

    signal_sets = []

    for variant in variants:

        signals = detect_behavioral_signals(
            variant
        )

        signal_sets.append(
            set(signals)
        )

    base = signal_sets[0]

    similarities = []

    for current in signal_sets:

        union = len(base | current)

        if union == 0:
            similarities.append(1.0)
            continue

        similarities.append(
            len(base & current) / union
        )

    consistency = (
        sum(similarities)
        / len(similarities)
    )

    return round(consistency, 3)
