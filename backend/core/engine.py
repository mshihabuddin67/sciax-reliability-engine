from backend.core.perturbation import generate_variants
from backend.core.stability_engine import compute_dynamic_stability
from backend.core.fuzzy import best_fuzzy_match
from backend.core.behavioral_signals import detect_behavioral_signals
from backend.core.signal_strength import calculate_signal_strength
from backend.core.confidence_fusion import compute_final_confidence

from backend.core.intent_engine import classify_intent
from backend.core.intent_consistency import compute_intent_consistency
from backend.core.explainability import generate_explanations

from backend.core.sciax_calibration_core import (
    calibrate_confidence,
    compute_calibrated_stability_score,
    compute_uncertainty
)

from backend.app.config import (
    VIOLENCE_STRONG,
    CYBER_STRONG,
    FRAUD_STRONG,
    SAFE_CONTEXTS
)

# ==================================================
# NORMALIZATION
# ==================================================

def normalize_simple(text: str) -> str:
    text = text.lower().strip()
    text = text.replace("  ", " ")
    return text


# ==================================================
# ANALYSIS BUILDER
# ==================================================

def build_analysis(stability, risk, confidence):

    return {
        "stability_score": round(stability, 2),
        "risk_level": risk,
        "confidence_score": confidence,
        "uncertainty_score": round(1 - confidence, 2),
    }


def build_response(
    text,
    variants,
    intent,
    stability,
    risk,
    confidence
):

    return {
        "prompt": text,
        "variants": variants,
        "intent_classification": [intent],
        "analysis": build_analysis(
            stability,
            risk,
            confidence
        )
    }


# ==================================================
# S-CIAX ENGINE (UPGRADED CORE)
# ==================================================

def sciax_engine(prompt):

    text = normalize_simple(prompt)

    # --------------------------------------------------
    # SIGNALS
    # --------------------------------------------------
    signals = detect_behavioral_signals(text)
    signal_count = len(signals)

    signal_strength = calculate_signal_strength(signals)

    # --------------------------------------------------
    # INTENT + EXPLAINABILITY 
    # --------------------------------------------------
    intents = classify_intent(text)

    explanations = generate_explanations(text)

    intent_consistency = compute_intent_consistency(
        intents=intents,
        behavioral_signals=signals,
        explainability=explanations
    )

    # --------------------------------------------------
    # VARIANTS + STABILITY
    # --------------------------------------------------
    variants = generate_variants(text)
    stability = compute_dynamic_stability(variants)

    # ==================================================
    # SAFE CONTEXT
    # ==================================================
    for safe in SAFE_CONTEXTS:
        if safe.lower() in text:

            stability = 0.90

            confidence = compute_final_confidence(
                stability=stability,
                signal_strength=0.0,
                behavioral_signals_count=0,
                intent_consistency=intent_consistency
                safe_override=True
            )

            return build_response(
                text,
                variants,
                "non-malicious",
                stability,
                "Low",
                confidence
            )

    # ==================================================
    # HARD VIOLENCE
    # ==================================================
    for v in VIOLENCE_STRONG:
        if v.lower() in text:

            stability = 0.85

            confidence = compute_final_confidence(
                stability=stability,
                signal_strength=signal_strength,
                behavioral_signals_count=signal_count,
                intent_consistency=intent_consistency
                strong_match=True
            )

            return build_response(
                text,
                variants,
                "violent_threat",
                stability,
                "High",
                confidence
            )

    # ==================================================
    # FUZZY MATCH
    # ==================================================
    match, score = best_fuzzy_match(
        text,
        VIOLENCE_STRONG,
        threshold=0.82
    )

    if match:

        confidence = compute_final_confidence(
            stability=score,
            signal_strength=signal_strength,
            behavioral_signals_count=signal_count,
            fuzzy_score=score,
            intent_consistency=intent_consistency
        )

        response = build_response(
            text,
            variants,
            "violent_threat",
            score,
            "High",
            confidence
        )

        response["fuzzy_match"] = {
            "matched_pattern": match,
            "similarity_score": score
        }

        return response

    # ==================================================
    # CYBER CHECK
    # ==================================================
    for c in CYBER_STRONG:
        if c.lower() in text:

            stability = 0.80

            confidence = compute_final_confidence(
                stability=stability,
                signal_strength=signal_strength,
                behavioral_signals_count=signal_count,
                intent_consistency=intent_consistency
                strong_match=True
            )

            return build_response(
                text,
                variants,
                "cyber_intrusion",
                stability,
                "High",
                confidence
            )

    # ==================================================
    # FRAUD CHECK
    # ==================================================
    for f in FRAUD_STRONG:
        if f.lower() in text:

            stability = 0.80

            confidence = compute_final_confidence(
                stability=stability,
                signal_strength=signal_strength,
                behavioral_signals_count=signal_count,
                intent_consistency=intent_consistency
                strong_match=True
            )

            return build_response(
                text,
                variants,
                "fraud",
                stability,
                "High",
                confidence
            )

    # ==================================================
    # DEFAULT LOGIC
    # ==================================================

    if stability > 0.75:
        risk = "Low"
    elif stability > 0.55:
        risk = "Medium"
    else:
        risk = "High"

    confidence = compute_final_confidence(
        stability=stability,
        signal_strength=signal_strength,
        behavioral_signals_count=signal_count,
        fuzzy_score=0.0,
        intent_consistency=intent_consistency
        strong_match=False,
        safe_override=False
    )


    return build_response(
        text,
        variants,
        "unknown_or_safe",
        stability,
        risk,
        confidence
    )
