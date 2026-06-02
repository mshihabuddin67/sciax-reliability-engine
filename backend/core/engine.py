from backend.core.perturbation import generate_variants
from backend.core.metrics import compute_stability_score
from backend.core.fuzzy import best_fuzzy_match
from backend.core.behavioral_signals import detect_behavioral_signals
from backend.core.confidence import calculate_confidence
from backend.app.config import (
    VIOLENCE_STRONG,
    CYBER_STRONG,
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
        "uncertainty_score": round(1 - confidence, 2)
    }


# ==================================================
# S-CIAX ENGINE
# ==================================================

def sciax_engine(prompt):

    text = normalize_simple(prompt)

    # -----------------------------
    # SIGNALS
    # -----------------------------
    signals = detect_behavioral_signals(text)
    signal_count = len(signals)

    # -----------------------------
    # VARIANTS + STABILITY
    # -----------------------------
    variants = generate_variants(text)
    stability = compute_stability_score(variants)

    # ==================================================
    # SAFE CONTEXT (DETERMINISTIC OVERRIDE)
    # ==================================================
    for safe in SAFE_CONTEXTS:

        if safe.lower() in text:

            stability = 0.90

            confidence = calculate_confidence(
                stability=stability,
                behavioral_signals_count=0,
                strong_match=False,
            
            )

            return {
                "prompt": text,
                "variants": variants,
                "analysis": build_analysis(
                    stability,
                    "Low",
                    confidence
                )
            }

    # ==================================================
    # HARD VIOLENCE CHECK
    # ==================================================
    for v in VIOLENCE_STRONG:

        if v.lower() in text:

            stability = 0.15

            confidence = calculate_confidence(
                stability=stability,
                behavioral_signals_count=signal_count,
                strong_match=True,
                
            )

            return {
                "prompt": text,
                "variants": variants,
                "analysis": build_analysis(
                    stability,
                    "High",
                    confidence
                )
            }

    # ==================================================
    # FUZZY MATCH CHECK
    # ==================================================
    match, score = best_fuzzy_match(
        text,
        VIOLENCE_STRONG,
        threshold=0.82
    )

    if match:

        confidence = calculate_confidence(
            stability=0.20,
            behavioral_signals_count=signal_count,
            fuzzy_score=score,
            
        )

        return {
            "prompt": text,
            "variants": variants,
            "analysis": build_analysis(
                0.20,
                "High",
                confidence
            ),
            "fuzzy_match": {
                "matched_pattern": match,
                "similarity_score": score
            }
        }

    # ==================================================
    # CYBER CHECK
    # ==================================================
    for c in CYBER_STRONG:

        if c.lower() in text:

            stability = 0.25

            confidence = calculate_confidence(
                stability=stability,
                behavioral_signals_count=signal_count,
                strong_match=True,
                
            )

            return {
                "prompt": text,
                "variants": variants,
                "analysis": build_analysis(
                    stability,
                    "High",
                    confidence
                )
            }

    # ==================================================
    # DEFAULT LOGIC
    # ==================================================
    if stability > 0.75:
        risk = "Low"
    elif stability > 0.55:
        risk = "Medium"
    else:
        risk = "High"

    confidence = calculate_confidence(
        stability=stability,
        behavioral_signals_count=signal_count,
        
    )

    return {
        "prompt": text,
        "variants": variants,
        "analysis": build_analysis(
            stability,
            risk,
            confidence
        )
            }
