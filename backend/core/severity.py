from backend.core.signal_weights import (
    calculate_signal_weight
)

def calculate_severity(signals):

    raw_score = calculate_signal_weight(signals)

    severity = max(
        0.0,
        min(raw_score, 1.0)
    )

    return round(severity, 2)
