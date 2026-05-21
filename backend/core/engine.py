from backend.core.perturbation import (
    generate_variants
)

from backend.core.metrics import (
    compute_stability_score
)


def sciax_engine(prompt):

    variants = generate_variants(prompt)

    stability = compute_stability_score(
        variants
    )

    risk = (

        "Low"

        if stability > 0.75

        else "Medium"

        if stability > 0.55

        else "High"
    )

    return {

        "prompt": prompt,

        "variants": variants,

        "stability_score":
            round(stability, 2),

        "risk_level":
            risk
    }
