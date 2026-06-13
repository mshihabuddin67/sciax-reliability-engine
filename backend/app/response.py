# ==================================================
# S-CIAX RESPONSE BUILDER (UPGRADED)
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

    analysis = engine_output.get("analysis", {})

    risk_level = analysis.get("risk_level", "Unknown")
    stability = analysis.get("stability_score", 0.50)
    confidence = analysis.get("confidence_score", 0.50)
    uncertainty = analysis.get("uncertainty_score", 0.50)

    # ==================================================
    # RECOMMENDED ACTION (IMPROVED LOGIC)
    # ==================================================

    if risk_level == "Critical":
        action = "block_immediately"

    elif risk_level == "High":
        action = "escalate_for_review"

    elif risk_level == "Medium":
        action = "monitor"

    else:
        action = "allow"

    # ==================================================
    # RISK QUALITY TAG (NEW INSIGHT LAYER)
    # ==================================================

    if confidence > 0.80 and uncertainty < 0.25:
        risk_quality = "high_certainty"

    elif uncertainty > 0.50:
        risk_quality = "ambiguous"

    else:
        risk_quality = "standard"

    # ==================================================
    # CLEAN DUPLICATES
    # ==================================================

    behavioral_signals = list(dict.fromkeys(behavioral_signals))
    intent_classification = list(dict.fromkeys(intent_classification))
    explainability = list(dict.fromkeys(explainability))

    # ==================================================
    # FINAL RESPONSE
    # ==================================================

    return {

        "input": input_text,

        "language_profile": language_profile,

        "behavioral_signals": behavioral_signals,

        "intent_classification": intent_classification,

        "risk_assessment": {

            "level": risk_level,

            "stability_score": round(stability, 2),

            "confidence_score": round(confidence, 2),

            "uncertainty_score": round(uncertainty, 2),

            # NEW LAYER
            "risk_quality": risk_quality
        },

        "explainability": explainability,

        "recommended_action": action
    }
