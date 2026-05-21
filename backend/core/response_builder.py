def build_response(
    input_text,
    engine_output,
    behavioral_signals,
    intent_classification,
    language_profile,
    explainability
):

    confidence_score = 0.91

    if engine_output["risk_level"] == "Medium":
        confidence_score = 0.72

    elif engine_output["risk_level"] == "Low":
        confidence_score = 0.35

    return {

        "input": input_text,

        "language_profile":
            language_profile,

        "behavioral_signals":
            behavioral_signals,

        "intent_classification":
            intent_classification,

        "risk_assessment": {

            "level":
                engine_output["risk_level"],

            "confidence_score":
                confidence_score,

            "uncertainty_score":
                round(
                    1 - confidence_score,
                    2
                )
        },

        "stability_analysis": {

            "stability_score":
                engine_output[
                    "stability_score"
                ],

            "conflict_escalation":

                "High"

                if engine_output[
                    "risk_level"
                ] == "High"

                else "Low"
        },

        "explainability_matrix":
            explainability,

        "meta": {

            "system_mode":
                "hybrid_light",

            "engine":
                "S-CIAX"
        }
    }
