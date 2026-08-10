from backend.core.normalization import normalize_text
from backend.core.language_profiles import detect_language_profile

from backend.core.perturbation import generate_variants
from backend.core.stability_engine import compute_dynamic_stability
from backend.core.fuzzy import best_fuzzy_match
from backend.core.behavioral_signals import detect_behavioral_signals
from backend.core.signal_strength import calculate_signal_strength
from backend.core.confidence_fusion import compute_final_confidence
from backend.core.risk_fusion import compute_final_risk

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
    SOCIAL_ENGINEERING_STRONG,
    CREDENTIAL_THEFT_STRONG,
    HARASSMENT_STRONG,
    COERCION_STRONG,
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

def build_analysis(
    stability,
    risk,
    confidence,
    intent_consistency
):

    return {
        "stability_score": round(stability, 2),
        "risk_level": risk,
        "confidence_score": confidence,
        "intent_consistency": round(intent_consistency, 2),
        "uncertainty_score": round(1 - confidence, 2),
    }


def build_response(
    text,
    variants,
    intent,
    stability,
    risk,
    confidence,
    intent_consistency,
    language_profile
):

    return {
        "prompt": text,
        "language_profile": language_profile,
        "variants": variants,
        "intent_classification": [intent],
        "analysis": build_analysis(
            stability,
            risk,
            confidence, 
            intent_consistency
        )
    }


# ==================================================
# S-CIAX ENGINE (UPGRADED CORE)
# ==================================================

def sciax_engine(prompt):

    text = normalize_text(prompt)
    
    language_profile = detect_language_profile(text)

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

    explanations = generate_explanations(
        text=text,
        intents=intents,
        behavioral_signals=signals
    )

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
    # SAFE CONTEXT DETECTION 
    # ==================================================

    safe_detected = False

    for safe in SAFE_CONTEXTS:
        if safe.lower() in text:
            safe_detected = True
            break

    # ==================================================
    # HARD VIOLENCE
    # ==================================================
    for v in VIOLENCE_STRONG:
        if v.lower() in text:

            

            confidence = compute_final_confidence(
                stability=stability,
                signal_strength=signal_strength,
                behavioral_signals_count=signal_count,
                intent_consistency=intent_consistency,
                strong_match=True
            )

            risk_result = compute_final_risk(
                intents=intents,
                signal_strength=signal_strength,
                confidence=confidence,
                stability=stability,
                intent_consistency=intent_consistency,
            )

            risk = risk_result["risk_level"]
            
            return build_response(
                text,
                variants,
                "violent_threat",
                stability,
                risk,
                confidence,
                intent_consistency
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
            intent_consistency=intent_consistency,
        )

        risk_result = compute_final_risk(
            intents=intents,
            signal_strength=signal_strength,
            confidence=confidence,
            stability=score,
            intent_consistency=intent_consistency,
        )

        risk = risk_result["risk_level"]
        
        response = build_response(
            text,
            variants,
            "violent_threat",
            score,
            risk,
            confidence,
            intent_consistency
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

            

            confidence = compute_final_confidence(
                stability=stability,
                signal_strength=signal_strength,
                behavioral_signals_count=signal_count,
                intent_consistency=intent_consistency,
                strong_match=True
            )

            risk_result = compute_final_risk(
                intents=intents,
                signal_strength=signal_strength,
                confidence=confidence,
                stability=stability,
                intent_consistency=intent_consistency,
            )

            risk = risk_result["risk_level"]
            
            return build_response(
                text,
                variants,
                "cyber_intrusion",
                stability,
                risk,
                confidence,
                intent_consistency
            )

    # ==================================================
    # FRAUD CHECK
    # ==================================================
    for f in FRAUD_STRONG:
        if f.lower() in text:

            

            confidence = compute_final_confidence(
                stability=stability,
                signal_strength=signal_strength,
                behavioral_signals_count=signal_count,
                intent_consistency=intent_consistency,
                strong_match=True
            )

            risk_result = compute_final_risk(
                intents=intents,
                signal_strength=signal_strength,
                confidence=confidence,
                stability=stability,
                intent_consistency=intent_consistency,
            )

            risk = risk_result["risk_level"]
            
            return build_response(
                text,
                variants,
                "fraud",
                stability,
                risk,
                confidence,
                intent_consistency
            )

    # ==================================================
    # SOCIAL ENGINEERING CHECK
    # ==================================================

    for social in SOCIAL_ENGINEERING_STRONG:
        if social.lower() in text:

            confidence = compute_final_confidence(
                stability=stability,
                signal_strength=signal_strength,
                behavioral_signals_count=signal_count,
                intent_consistency=intent_consistency,
                strong_match=True
            )

            risk_result = compute_final_risk(
                intents=intents,
                signal_strength=signal_strength,
                confidence=confidence,
                stability=stability,
                intent_consistency=intent_consistency,
            )

            return build_response(
                text,
                variants,
                "social_engineering",
                stability,
                risk_result["risk_level"],
                confidence,
                intent_consistency
            )


    # ==================================================
    # CREDENTIAL THEFT CHECK
    # ==================================================

    for credential in CREDENTIAL_THEFT_STRONG:
        if credential.lower() in text:

            confidence = compute_final_confidence(
                stability=stability,
                signal_strength=signal_strength,
                behavioral_signals_count=signal_count,
                intent_consistency=intent_consistency,
                strong_match=True
            )

            risk_result = compute_final_risk(
                intents=intents,
                signal_strength=signal_strength,
                confidence=confidence,
                stability=stability,
                intent_consistency=intent_consistency,
            )

            return build_response(
                text,
                variants,
                "credential_theft",
                stability,
                risk_result["risk_level"],
                confidence,
                intent_consistency
            )


    # ==================================================
    # HARASSMENT CHECK
    # ==================================================

    for harassment in HARASSMENT_STRONG:
        if harassment.lower() in text:

            confidence = compute_final_confidence(
                stability=stability,
                signal_strength=signal_strength,
                behavioral_signals_count=signal_count,
                intent_consistency=intent_consistency,
                strong_match=True
            )

            risk_result = compute_final_risk(
                intents=intents,
                signal_strength=signal_strength,
                confidence=confidence,
                stability=stability,
                intent_consistency=intent_consistency,
            )

            return build_response(
                text,
                variants,
                "harassment",
                stability,
                risk_result["risk_level"],
                confidence,
                intent_consistency
            )


    # ==================================================
    # COERCION CHECK
    # ==================================================

    for coercion in COERCION_STRONG:
        if coercion.lower() in text:

            confidence = compute_final_confidence(
                stability=stability,
                signal_strength=signal_strength,
                behavioral_signals_count=signal_count,
                intent_consistency=intent_consistency,
                strong_match=True
            )

            risk_result = compute_final_risk(
                intents=intents,
                signal_strength=signal_strength,
                confidence=confidence,
                stability=stability,
                intent_consistency=intent_consistency,
            )

            return build_response(
                text,
                variants,
                "coercion",
                stability,
                risk_result["risk_level"],
                confidence,
                intent_consistency
            )

    # ==================================================
    # DEFAULT LOGIC
    # ==================================================

    confidence = compute_final_confidence(
        stability=stability,
        signal_strength=signal_strength,
        behavioral_signals_count=signal_count,
        fuzzy_score=0.0,
        intent_consistency=intent_consistency,
        strong_match=False,
        safe_override=safe_detected
    )
    
    risk_result = compute_final_risk(
        intents=intents,
        signal_strength=signal_strength,
        confidence=confidence,
        stability=stability,
        intent_consistency=intent_consistency,
    )

    risk = risk_result["risk_level"]
    
    return build_response(
        text,
        variants,
        "unknown_or_safe",
        stability,
        risk,
        confidence,
        intent_consistency
    )
