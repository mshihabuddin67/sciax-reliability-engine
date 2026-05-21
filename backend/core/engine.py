from backend.core.perturbation import generate_variants
from backend.core.metrics import compute_stability_score

from backend.core.config import (
    VIOLENCE_STRONG,
    CYBER_STRONG
)

# ==================================================
# S-CIAX HYBRID ENGINE
# ==================================================

def sciax_engine(prompt):

    text = prompt.lower()

    variants = generate_variants(text)

    stability = compute_stability_score(variants)

    # --------------------------------------------------
    # HARD VIOLENCE CHECK
    # --------------------------------------------------

    for v in VIOLENCE_STRONG:
        if v in text:
            return {

                "prompt": text,
                "variants": variants,

                "stability_score": 0.15,
                "risk_level": "High"
            }

    # --------------------------------------------------
    # CYBER RISK CHECK
    # --------------------------------------------------

    for c in CYBER_STRONG:
        if c in text:
            return {

                "prompt": text,
                "variants": variants,

                "stability_score": 0.25,
                "risk_level": "High"
            }

    # --------------------------------------------------
    # DEFAULT LOGIC
    # --------------------------------------------------

    if stability > 0.75:
        risk = "Low"

    elif stability > 0.55:
        risk = "Medium"

    else:
        risk = "High"

    return {

        "prompt": text,
        "variants": variants,

        "stability_score": round(stability, 2),
        "risk_level": risk
    }
