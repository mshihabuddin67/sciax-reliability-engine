def decide_action(risk_score):

    if risk_score >= 0.85:
        return {
            "action": "notify_moderator",
            "priority": "P1"
        }

    elif risk_score >= 0.6:
        return {
            "action": "flag_for_review",
            "priority": "P2"
        }

    else:
        return {
            "action": "allow",
            "priority": "P3"
        }
