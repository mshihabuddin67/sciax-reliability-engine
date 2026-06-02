# ==================================================
# S-CIAX SIGNAL WEIGHTS
# ==================================================

SIGNAL_WEIGHTS = {

    "violent aggression": 0.30,

    "cyber intrusion intent": 0.25,

    "fraud intent": 0.22,

    "credential theft": 0.22,

    "social engineering": 0.20,

    "coercion": 0.18,

    "harassment": 0.15,

    "target-directed aggression": 0.12,

    "first-person threat language": 0.10,

    "implicit threat escalation": 0.08,

    "benign optimization context": -0.25
}


def calculate_signal_weight(signals):

    score = 0.0

    for signal in signals:

        score += SIGNAL_WEIGHTS.get(
            signal,
            0.0
        )

    return round(
        max(score, 0.0),
        2
    )
