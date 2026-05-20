WEIGHTS = {
    "risk": 0.4,
    "behavior": 0.3,
    "intent": 0.2,
    "language": 0.1
}


def compute_fused_risk(risk, behavior_score, intent_score, language_score):

    score = (
        risk * WEIGHTS["risk"] +
        behavior_score * WEIGHTS["behavior"] +
        intent_score * WEIGHTS["intent"] +
        language_score * WEIGHTS["language"]
    )

    return round(score, 3)
