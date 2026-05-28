from backend.core.perturbation import generate_variants
from backend.core.metrics import compute_stability_score

from backend.app.config import (
    VIOLENCE_STRONG,
    CYBER_STRONG,
    SAFE_CONTEXTS
)

# ==================================================
# S-CIAX HYBRID ENGINE v2 STABLE
# ==================================================

def normalize_simple(text: str) -> str:

    text = text.lower().strip()

    # lightweight normalization
    text = text.replace("  ", " ")

    return text


# ==================================================
# CONFIDENCE CALCULATOR
# ==================================================

def compute_confidence(
    risk_level,
    stability
):

    # --------------------------------------------------
    # HIGH RISK
    # --------------------------------------------------

    if risk_level == "High":

        confidence = 0.90

    # --------------------------------------------------
    # MEDIUM RISK
    # --------------------------------------------------

    elif risk_level == "Medium":

        confidence = 0.65

    # --------------------------------------------------
    # LOW RISK
    # --------------------------------------------------

    else:

        confidence = 0.35 + (
            stability * 0.5
        )

    return round(
        min(confidence, 0.99),
        2
    )


# ==================================================
# MAIN ENGINE
# ==================================================

def sciax_engine(prompt):

    text = normalize_simple(prompt)

    variants = generate_variants(text)

    stability = compute_stability_score(
        variants
    )

    # --------------------------------------------------
    # SAFE CONTEXT CHECK
    # --------------------------------------------------

    for safe in SAFE_CONTEXTS:

        if safe.lower() in text:

            confidence = 0.96

            return {

                "prompt": text,

                "variants": variants,

                "stability_score": 0.92,

                "risk_level": "Low",

                "confidence_score": confidence,

                "uncertainty_score": round(
                    1 - confidence,
                    2
                )
            }

    # --------------------------------------------------
    # HARD VIOLENCE CHECK
    # --------------------------------------------------

    for v in VIOLENCE_STRONG:

        if v.lower() in text:

            confidence = 0.91

            return {

                "prompt": text,

                "variants": variants,

                "stability_score": 0.15,

                "risk_level": "High",

                "confidence_score": confidence,

                "uncertainty_score": round(
                    1 - confidence,
                    2
                )
            }

    # --------------------------------------------------
    # CYBER RISK CHECK
    # --------------------------------------------------

    for c in CYBER_STRONG:

        if c.lower() in text:

            confidence = 0.88

            return {

                "prompt": text,

                "variants": variants,

                "stability_score": 0.25,

                "risk_level": "High",

                "confidence_score": confidence,

                "uncertainty_score": round(
                    1 - confidence,
                    2
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

    confidence = compute_confidence(
        risk,
        stability
    )

    # --------------------------------------------------
    # FINAL OUTPUT
    # --------------------------------------------------

    return {

        "prompt": text,

        "variants": variants,

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
