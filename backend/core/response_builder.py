def build_response(
    input_text,
    engine_output,
    behavioral_signals,
    intent_classification,
    language_profile,
    explainability
):

    analysis = engine_output.get(
        "analysis",
        {}
    )

    risk_level = analysis.get(
        "risk_level",
        "Unknown"
    )

    stability = analysis.get(
        "stability_score",
        0.50
    )

    confidence = analysis.get(
        "confidence_score",
        0.50
    )

    intent_consistency = analysis.get(
    "intent_consistency",
    0.50
    )

    uncertainty = analysis.get(
        "uncertainty_score",
        round(1 - confidence, 2)
    )

    # recommended action
    if risk_level == "High":
        action = "escalate_for_review"

    elif risk_level == "Medium":
        action = "monitor"

    else:
        action = "allow"

    # remove duplicates
    behavioral_signals = list(dict.fromkeys(behavioral_signals))
    intent_classification = list(dict.fromkeys(intent_classification))
    explainability = list(dict.fromkeys(explainability))

    return {

        "input": input_text,

        "language_profile": language_profile,

        "behavioral_signals": behavioral_signals,

        "intent_classification": intent_classification,

        "risk_assessment": {

            "level": risk_level,

            "stability_score": stability,

            "confidence_score": confidence,

            "intent_consistency": intent_consistency,

            "uncertainty_score": uncertainty
        },

        "explainability": explainability,

        "recommended_action": action
    }
