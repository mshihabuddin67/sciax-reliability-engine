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
    # SAFE ANALYSIS ACCESS
    # --------------------------------------------------

    analysis = engine_output.get(
        "analysis",
        {}
    )

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
    # REMOVE DUPLICATES
    # --------------------------------------------------

    behavioral_signals = list(
        dict.fromkeys(behavioral_signals)
    )

    intent_classification = list(
        dict.fromkeys(intent_classification)
    )

    explainability = list(
        dict.fromkeys(explainability)
    )

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

        "risk_assessment": {

            "level":
                risk_level,

            "stability_score":
                analysis.get(
                    "stability_score",
                    0.50
                ),

            "confidence_score":
                analysis.get(
                    "confidence_score",
                    0.50
                ),

            "uncertainty_score":
                analysis.get(
                    "uncertainty_score",
                    0.50
                )
        },

        "explainability":
            explainability,

        "recommended_action":
            action
    }
