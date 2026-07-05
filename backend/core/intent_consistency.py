# ==================================================
# S-CIAX INTENT CONSISTENCY ENGINE V3
# ==================================================

def compute_intent_consistency(
    intents,
    behavioral_signals,
    explainability=None
):
    """
    Computes how consistent the detected intent is with
    behavioral evidence and explanations.

    Returns:
        float (0.0 - 1.0)
    """

    try:

        if explainability is None:
            explainability = []

        score = 0.50

        intents = set(intents)
        signals = set(behavioral_signals)

        # ==================================================
        # SAFE
        # ==================================================

        if "non-malicious" in intents:

            if "benign optimization context" in signals:
                score += 0.35

            if any(
                "safe" in e.lower()
                for e in explainability
            ):
                score += 0.10

        # ==================================================
        # VIOLENCE
        # ==================================================

        if "violent_threat" in intents:

            if "violent aggression" in signals:
                score += 0.20

            if "target-directed aggression" in signals:
                score += 0.10

            if "implicit threat escalation" in signals:
                score += 0.10

            if "first-person threat language" in signals:
                score += 0.10

        # ==================================================
        # CYBER
        # ==================================================

        if "cyber_intrusion" in intents:

            if "cyber intrusion intent" in signals:
                score += 0.30

        # ==================================================
        # FRAUD
        # ==================================================

        if "fraud" in intents:

            if "fraud intent" in signals:
                score += 0.30

        # ==================================================
        # SOCIAL ENGINEERING
        # ==================================================

        if "social_engineering" in intents:

            if "social engineering" in signals:
                score += 0.25

        # ==================================================
        # CREDENTIAL THEFT
        # ==================================================

        if "credential_theft" in intents:

            if "credential theft" in signals:
                score += 0.25

        # ==================================================
        # HARASSMENT
        # ==================================================

        if "harassment" in intents:

            if "harassment" in signals:
                score += 0.20

        # ==================================================
        # COERCION
        # ==================================================

        if "coercion" in intents:

            if "coercion" in signals:
                score += 0.20

        # ==================================================
        # UNKNOWN
        # ==================================================

        if "unknown_or_safe" in intents:

            if len(signals) == 0:
                score += 0.20
            else:
                score -= 0.20

        # ==================================================
        # NORMALIZE
        # ==================================================

        score = max(0.0, min(score, 1.0))

        return round(score, 3)

    except Exception as e:

        print(f"[INTENT CONSISTENCY ERROR] {e}")

        return 0.50
