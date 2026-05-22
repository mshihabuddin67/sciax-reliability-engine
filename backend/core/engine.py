from backend.core.perturbation import generate_variants
from backend.core.metrics import compute_stability_score

from backend.app.config import (
    VIOLENCE_STRONG,
    CYBER_STRONG,
    SAFE_CONTEXTS
)

# ==================================================
# S-CIAX HYBRID ENGINE (STABLE VERSION)
# ==================================================

def normalize_simple(text: str) -> str:

    text = text.lower().strip()

    # lightweight normalization
    text = text.replace("  ", " ")

    return text


def sciax_engine(prompt):

    text = normalize_simple(prompt)

    variants = generate_variants(text)

    stability = compute_stability_score(
        variants
    )

    # --------------------------------------------------
    # SAFE CONTEXT CHECK (FIRST PRIORITY)
    # --------------------------------------------------

    for safe in SAFE_CONTEXTS:

        if safe.lower() in text:

            return {

                "prompt": text,

                "variants": variants,

                "stability_score": 0.92,

                "risk_level": "Low"
            }

    # --------------------------------------------------
    # HARD VIOLENCE CHECK
    # --------------------------------------------------

    for v in VIOLENCE_STRONG:

        if v.lower() in text:

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

        if c.lower() in text:

            return {

                "prompt": text,

                "variants": variants,

                "stability_score": 0.25,

                "risk_level": "High"
            }

    # --------------------------------------------------
    # CONTEXT-AWARE DEFAULT LOGIC
    # --------------------------------------------------

    if stability > 0.75:

        risk = "Low"

    elif stability > 0.55:

        risk = "Medium"

    else:

        risk = "Low"

    return {

        "prompt": text,

        "variants": variants,

        "stability_score": round(
            stability,
            2
        ),

        "risk_level": risk
        }
