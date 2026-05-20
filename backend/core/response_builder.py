from core.weights import compute_fused_risk
from core.policy_engine import decide_action


def build_response(
    input_text,
    engine_output,
    behavioral_signals,
    intent_classification,
    language_profile,
    explainability
):

    # Convert signals into numeric scores
    risk_score = 1.0 if engine_output["risk_level"] == "High" else 0.5
    behavior_score = 0.8 if behavioral_signals else 0.3
    intent_score = 0.9 if "violent_threat" in intent_classification else 0.4
    language_score = 0.6 if language_profile else 0.5

    # Fusion
    fused_risk = compute_fused_risk(
        risk_score,
        behavior_score,
        intent_score,
        language_score
    )

    # Policy decision
    action = decide_action(fused_risk)

    return {
        "input": input_text,

        "language_profile": language_profile,

        "behavioral_signals": behavioral_signals,

        "intent_classification": intent_classification,

        "risk_assessment": {
            "level": engine_output["risk_level"],
            "confidence_score": round(fused_risk, 2),
            "uncertainty_score": round(1 - fused_risk, 2)
        },

        "stability_analysis": {
            "stability_score": engine_output["stability_score"],
            "conflict_escalation": "High" if fused_risk > 0.7 else "Low"
        },

        "explainability_matrix": explainability,

        "action_recommendation": action,

        "meta": {
            "system_mode": "hybrid_v2_fusion",
            "fusion_score": fused_risk
        }
    }
