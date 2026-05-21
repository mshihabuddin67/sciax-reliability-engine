def build_response(

    input_text,

    engine_output,

    behavioral_signals,

    intent_classification,

    language_profile,

    explainability
):

    return {

        "input": input_text,

        "language_profile":
            language_profile,

        "behavioral_signals":
            behavioral_signals,

        "intent_classification":
            intent_classification,

        "engine_output":
            engine_output,

        "risk_assessment": {

            "level":
                engine_output.get(
                    "risk_level",
                    "Unknown"
                ),

            "stability_score":
                engine_output.get(
                    "stability_score",
                    0.5
                )
        },

        "explainability":
            explainability
    }
