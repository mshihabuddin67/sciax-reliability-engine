# ==================================================
# S-CIAX SIGNAL WEIGHTS (UPGRADED)
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

    # benign reduces risk pressure
    "benign optimization context": -0.25
}


def calculate_signal_strength(signals):

    try:
        if not signals or not isinstance(signals, list):
            return 0.0

        score = 0.0

        for signal in signals:

            if not signal:
                continue

            weight = SIGNAL_WEIGHTS.get(signal, 0.0)

            # ==================================================
            # NON-LINEAR BOOST (HIGH RISK SIGNALS)
            # ==================================================
            if weight >= 0.20:
                weight = weight ** 1.15

            score += weight

        # ==================================================
        # INTERACTION BOOST (IMPORTANT COMBOS)
        # ==================================================

        if (
            "fraud intent" in signals and
            "social engineering" in signals
        ):
            score *= 1.15

        if (
            "cyber intrusion intent" in signals and
            "credential theft" in signals
        ):
            score *= 1.20

        # ==================================================
        # NORMALIZATION (0–1 SAFE BOUND)
        # ==================================================

        normalized = score / max(len(signals), 1)

        return round(
            max(0.0, min(normalized, 1.0)),
            2
        )

    except Exception as e:
        # prevents Render 500 crash
        print(f"[S-CIAX SIGNAL ERROR]: {e}")
        return 0.0
