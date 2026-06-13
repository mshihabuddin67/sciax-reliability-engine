from backend.core.signal_strength import calculate_signal_strength


def calculate_severity(signals):

    raw_score = calculate_signal_strength(signals)

    severity = max(
        0.0,
        min(raw_score, 1.0)
    )

    return round(severity, 2)
