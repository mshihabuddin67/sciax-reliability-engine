from backend.core.perturbation import generate_variants
from backend.core.metrics import compute_stability_score
from backend.core.fuzzy import best_fuzzy_match
from backend.core.behavioral_signals import (
    detect_behavioral_signals
)

from backend.core.confidence import (
    calculate_confidence
)

from backend.app.config import (
    VIOLENCE_STRONG,
    CYBER_STRONG,
    SAFE_CONTEXTS
)

# ==================================================
# S-CIAX HYBRID ENGINE v3 STABLE
# ==================================================

def normalize_simple(text: str) -> str:

    text = text.lower().strip()

    # lightweight normalization
    text = text.replace("  ", " ")

    return text

# ==================================================
# ANALYSIS BUILDER
# ==================================================

def build_analysis(
    stability,
    risk,
    confidence
):

    return {

        "stability_score": round(
            stability,
            2
        ),

        "risk_level": risk,

        "confidence_score": confidence,

        "uncertainty_score": round(
            1 - confidence,
            2
        )
    }


# ==================================================
# MAIN ENGINE
# ==================================================

def sciax_engine(prompt):

    text = normalize_simple(prompt)
    signals = detect_behavioral_signals(
    text
)

signal_count = len(signals)

    variants = generate_variants(text)

    stability = compute_stability_score(
        variants
    )

    # --------------------------------------------------
    # SAFE CONTEXT CHECK
    # --------------------------------------------------

    for safe in SAFE_CONTEXTS:

        if safe.lower() in text:

            confidence = calculate_confidence(
    stability=0.92,
    behavioral_signals_count=0,
    strong_match=False
            )

            return {

                "prompt": text,

                "variants": variants,

                "analysis": build_analysis(
                    0.92,
                    "Low",
                    confidence
                )
            }

    # --------------------------------------------------
    # HARD VIOLENCE CHECK
    # --------------------------------------------------

    for v in VIOLENCE_STRONG:

        if v.lower() in text:

            confidence = calculate_confidence(
    stability=0.15,
    behavioral_signals_count=signal_count,
    strong_match=True
            )

            return {

                "prompt": text,

                "variants": variants,

                "analysis": build_analysis(
                    0.15,
                    "High",
                    confidence
                )
            }
    
    # --------------------------------------------------
    # FUZZY VIOLENCE CHECK
    # --------------------------------------------------

    match, score = best_fuzzy_match(
        text,
        VIOLENCE_STRONG,
        threshold=0.82
    )

    if match:

        confidence = calculate_confidence(
    stability=0.20,
    behavioral_signals_count=signal_count,
    fuzzy_score=score
        )

        return {

            "prompt": text,

            "variants": variants,

            "analysis": {

                "stability_score": 0.20,

                "risk_level": "High",

                "confidence_score": confidence,

                "uncertainty_score": round(
                    1 - confidence,
                    2
                )
            },

            "fuzzy_match": {

                "matched_pattern": match,

                "similarity_score": score
            }
        }
    
    # --------------------------------------------------
    # CYBER RISK CHECK
    # --------------------------------------------------

    for c in CYBER_STRONG:

        if c.lower() in text:

            confidence = calculate_confidence(
    stability=0.25,
    behavioral_signals_count=signal_count,
    strong_match=True
            )

            return {

                "prompt": text,

                "variants": variants,

                "analysis": build_analysis(
                    0.25,
                    "High",
                    confidence
                )
            }

    # --------------------------------------------------
    # DEFAULT CONTEXT-AWARE LOGIC
    # --------------------------------------------------

    if stability > 0.75:

        risk = "Low"

    elif stability > 0.55:

        risk = "Medium"

    else:

        risk = "High"

    # --------------------------------------------------
    # CONFIDENCE
    # --------------------------------------------------

    confidence = calculate_confidence(
    stability=stability,
    behavioral_signals_count=signal_count
    )

    # --------------------------------------------------
    # FINAL OUTPUT
    # --------------------------------------------------

    return {

        "prompt": text,

        "variants": variants,

        "analysis": build_analysis(
            stability,
            risk,
            confidence
        )
            }
