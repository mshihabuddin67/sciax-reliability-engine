# ==================================================
# S-CIAX RESPONSE BUILDER
# ==================================================

def build_response(

    input_text,

    engine_output,

    behavioral_signals,

    intent_classification,

    language_profile,

    explainability
):

    # --------------------------------------------------
    # SAFE ACCESS TO ANALYSIS BLOCK
    # --------------------------------------------------

    analysis = engine_output.get(
        "analysis",
        {}
    )

    # --------------------------------------------------
    # RISK LEVEL
    # --------------------------------------------------

    risk_level = analysis.get(
        "risk_level",
        "Unknown"
    )

    # --------------------------------------------------
    # RECOMMENDED ACTION
    # --------------------------------------------------

    if risk_level == "High":

        action = "escalate_for_review"

    elif risk_level == "Medium":

        action = "monitor"

    else:

        action = "allow"

    # --------------------------------------------------
    # FINAL RESPONSE
    # --------------------------------------------------

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
                risk_level,

            "stability_score":
                analysis.get(
                    "stability_score",
                    0.5
                ),

            "confidence_score":
                analysis.get(
                    "confidence_score",
                    0.5
                ),

            "uncertainty_score":
                analysis.get(
                    "uncertainty_score",
                    0.5
                )
        },

        "explainability":
            explainability,

        "recommended_action":
            action
    }
