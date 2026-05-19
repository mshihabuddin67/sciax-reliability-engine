from core.behavioral_signals import detect_behavioral_signals
from core.intent_engine import classify_intent
from core.explainability import generate_explainability
from core.confidence import (
    calibrate_confidence,
    calculate_uncertainty
)
from core.language_profiles import detect_language_profile


def build_response(
    input_text,
    normalized_text,
    risk_level,
    raw_confidence,
    stability_score,
    conflict_score
):

    confidence = calibrate_confidence(raw_confidence)

    response = {

        "input": input_text,

        "reconstructed_text": normalized_text,

        "language_profile":
            detect_language_profile(input_text),

        "behavioral_signals":
            detect_behavioral_signals(normalized_text),

        "intent_classification":
            classify_intent(normalized_text),

        "risk_assessment": {
            "level": risk_level,
            "confidence_score": confidence,
            "uncertainty_score":
                calculate_uncertainty(confidence)
        },

        "stability_analysis": {
            "stability_score": stability_score,
            "conflict_escalation":
                "Elevated"
                if conflict_score > 0.7
                else "Minimal"
        },

        "explainability_matrix":
            generate_explainability(normalized_text)
    }

    return response
