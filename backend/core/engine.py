from backend.core.perturbation import (
    generate_variants
)

from backend.core.metrics import (
    compute_stability_score
)


SAFE_CONTEXTS = [

    "sleep schedule",
    "study hack",
    "life hack",
    "productivity hack",
    "gaming strategy",
    "game level"
]


HIGH_RISK_PATTERNS = [

    "hack the system",
    "bypass security",
    "steal data",
    "exploit vulnerability",
    "kill you",
    "murder"
]


def sciax_engine(prompt):

    text = prompt.lower()

    variants = generate_variants(text)

    stability = compute_stability_score(
        variants
    )

    # ---------------------------------
    # SAFE CONTEXT OVERRIDE
    # ---------------------------------

    for safe in SAFE_CONTEXTS:

        if safe in text:

            return {

                "prompt": text,

                "variants": variants,

                "stability_score":
                    0.91,

                "risk_level":
                    "Low"
            }

    # ---------------------------------
    # HIGH RISK PATTERN
    # ---------------------------------

    for pattern in HIGH_RISK_PATTERNS:

        if pattern in text:

            return {

                "prompt": text,

                "variants": variants,

                "stability_score":
                    0.25,

                "risk_level":
                    "High"
            }

    # ---------------------------------
    # DEFAULT LOGIC
    # ---------------------------------

    risk = (

        "Low"

        if stability > 0.75

        else "Medium"

        if stability > 0.55

        else "Low"
    )

    return {

        "prompt": text,

        "variants": variants,

        "stability_score":
            round(stability, 2),

        "risk_level":
            risk
            }
