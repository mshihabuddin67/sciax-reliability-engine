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
from backend.core.evidence import analyze_evidence

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
# EVIDENCE-AWARE INTENT ADJUDICATION
# ==================================================

def resolve_evidence_intent(
    intents,
    evidence_result
):
    """
    Resolve candidate intents using Evidence Engine output.

    Design:
        - Context can correct isolated lexical false positives.
        - Strong multi-intent harmful evidence is preserved.
        - Direct threat/cyber evidence is not overridden by
          a benign contextual prefix.
        - Existing risk/confidence engines remain unchanged.
    """

    if not isinstance(evidence_result, dict):
        return intents[0] if intents else "unknown_or_safe"

    intent_evidence = evidence_result.get(
        "intent_evidence",
        {}
    )

    evidence_items = evidence_result.get(
        "evidence",
        []
    )

    if not isinstance(intent_evidence, dict):
        return intents[0] if intents else "unknown_or_safe"

    if not intent_evidence:
        return intents[0] if intents else "unknown_or_safe"

    # --------------------------------------------------
    # Candidate scores
    # --------------------------------------------------

    scores = {}

    for intent, data in intent_evidence.items():

        if not isinstance(data, dict):
            continue

        score = data.get(
            "evidence_score",
            0.0
        )

        try:
            score = float(score)
        except (TypeError, ValueError):
            score = 0.0

        scores[intent] = score

    if not scores:
        return intents[0] if intents else "unknown_or_safe"

    # --------------------------------------------------
    # Benign contextual evidence
    # --------------------------------------------------

    benign_score = scores.get(
        "non-malicious",
        0.0
    )

    # --------------------------------------------------
    # Harmful candidates
    # --------------------------------------------------

    harmful_intents = {
        "violent_threat",
        "cyber_intrusion",
        "fraud",
        "social_engineering",
        "credential_theft",
        "harassment",
        "coercion",
    }

    harmful_scores = {
        intent: score
        for intent, score in scores.items()
        if intent in harmful_intents
    }

    # --------------------------------------------------
    # Detect contextual safety support
    # --------------------------------------------------

    has_strong_benign_context = False

    for item in evidence_items:

        if not isinstance(item, dict):
            continue

        if item.get("evidence_type") != "contextual_support":
            continue

        if item.get("intent") != "non-malicious":
            continue

        try:
            strength = float(
                item.get("strength", 0.0)
            )
        except (TypeError, ValueError):
            strength = 0.0

        if strength >= 0.90:
            has_strong_benign_context = True
            break

    # --------------------------------------------------
    # Contextual correction
    #
    # An isolated lexical credential/fraud candidate may
    # be corrected when strong defensive context exists.
    #
    # Multiple harmful intents indicate a more complex
    # malicious interpretation and must be preserved.
    # --------------------------------------------------

    if has_strong_benign_context:

        harmful_intent_names = set(
            harmful_scores.keys()
        )

        isolated_lexical_risk = harmful_intent_names.issubset(
            {
                "credential_theft",
                "fraud",
            }
        )

        if isolated_lexical_risk:
            return "non-malicious"

    # --------------------------------------------------
    # General benign comparison
    #
    # Only allow benign override when harmful evidence
    # is weak.
    # --------------------------------------------------

    strongest_harmful_score = max(
        harmful_scores.values(),
        default=0.0
    )

    if benign_score > strongest_harmful_score:
        return "non-malicious"

    # --------------------------------------------------
    # Preserve strongest harmful intent
    # --------------------------------------------------

    if harmful_scores:
        return max(
            harmful_scores,
            key=harmful_scores.get
        )

    # --------------------------------------------------
    # Fallback
    # --------------------------------------------------

    return max(
        scores,
        key=scores.get
    )

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
    language_profile,
    evidence_result=None
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
        ),

        "evidence": evidence_result
        
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
    # EVIDENCE ENGINE
    # --------------------------------------------------

    evidence_result = analyze_evidence(
        text=text,
        signals=signals,
        intents=intents,
        explanations=explanations
    )

    evidence_quality = evidence_result["global_evidence_quality"]
    contradiction_score = evidence_result["contradiction_score"]

    # --------------------------------------------------
    # EVIDENCE-AWARE INTENT ADJUDICATION
    # --------------------------------------------------

    resolved_intent = resolve_evidence_intent(
        intents=intents,
        evidence_result=evidence_result
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
                evidence_quality=evidence_quality,
                contradiction_score=contradiction_score,
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
                intent_consistency,
                language_profile,
                evidence_result
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
            evidence_quality=evidence_quality,
            contradiction_score=contradiction_score,
            strong_match=False
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
            intent_consistency,
            language_profile,
            evidence_result
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
                evidence_quality=evidence_quality,
                contradiction_score=contradiction_score,
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
                intent_consistency,
                language_profile,
                evidence_result 
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
                evidence_quality=evidence_quality,
                contradiction_score=contradiction_score,
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
                intent_consistency,
                language_profile, 
                evidence_result 
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
                evidence_quality=evidence_quality,
                contradiction_score=contradiction_score,
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
                intent_consistency,
                language_profile, 
                evidence_result 
            )


    # ==================================================
    # CREDENTIAL THEFT CHECK
    # ==================================================

    for credential in CREDENTIAL_THEFT_STRONG:
        if credential.lower() in text:

            if resolved_intent == "non-malicious":
                continue
            
            confidence = compute_final_confidence(
                stability=stability,
                signal_strength=signal_strength,
                behavioral_signals_count=signal_count,
                intent_consistency=intent_consistency,
                evidence_quality=evidence_quality,
                contradiction_score=contradiction_score,
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
                intent_consistency, 
                language_profile, 
                evidence_result 
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
                evidence_quality=evidence_quality,
                contradiction_score=contradiction_score,
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
                intent_consistency, 
                language_profile, 
                evidence_result 
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
                evidence_quality=evidence_quality,
                contradiction_score=contradiction_score,
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
                intent_consistency, 
                language_profile, 
                evidence_result 
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
        evidence_quality=evidence_quality,
        contradiction_score=contradiction_score,
        strong_match=False,
        safe_override=safe_detected
    )
    
    # --------------------------------------------------
    # Use evidence-resolved intent for final risk
    # --------------------------------------------------

    risk_intents = intents

    if resolved_intent == "non-malicious":
        risk_intents = ["non-malicious"]

    risk_result = compute_final_risk(
        intents=risk_intents,
        signal_strength=signal_strength,
        confidence=confidence,
        stability=stability,
        intent_consistency=intent_consistency,
    )

    risk = risk_result["risk_level"]

    return build_response(
        text,
        variants,
        resolved_intent,
        stability,
        risk,
        confidence,
        intent_consistency,
        language_profile,
        evidence_result
    )
