import math


# ==================================================
# TOKEN SIMILARITY
# ==================================================

def token_similarity(a: str, b: str) -> float:

    a_tokens = set(a.split())
    b_tokens = set(b.split())

    if not a_tokens and not b_tokens:
        return 1.0

    union = len(a_tokens | b_tokens)

    if union == 0:
        return 1.0

    return len(a_tokens & b_tokens) / union


# ==================================================
# LENGTH CONSISTENCY
# ==================================================

def length_consistency(base: str, variant: str) -> float:

    base_len = len(base.split())
    var_len = len(variant.split())

    diff = abs(base_len - var_len)

    return max(
        0.0,
        1 - diff / max(base_len, 1)
    )


# ==================================================
# DYNAMIC STABILITY ENGINE V3
# ==================================================

def compute_dynamic_stability(variants):
    """
    Dynamic Stability Engine V3

    Factors
    -------
    1. Variant uniqueness
    2. Token similarity
    3. Length consistency

    Output
    ------
    0.0 - 1.0
    """

    if not variants:
        return 0.0

    if len(variants) == 1:
        return 1.0

    base = variants[0]

    # ---------------------------------------
    # UNIQUENESS
    # ---------------------------------------

    uniqueness = (
        len(set(variants))
        / len(variants)
    )

    # ---------------------------------------
    # TOKEN SIMILARITY
    # ---------------------------------------

    token_scores = []

    for variant in variants:

        token_scores.append(
            token_similarity(
                base,
                variant
            )
        )

    token_score = (
        sum(token_scores)
        / len(token_scores)
    )

    # ---------------------------------------
    # LENGTH CONSISTENCY
    # ---------------------------------------

    length_scores = []

    for variant in variants:

        length_scores.append(
            length_consistency(
                base,
                variant
            )
        )

    length_score = (
        sum(length_scores)
        / len(length_scores)
    )

    # ---------------------------------------
    # FINAL SCORE
    # ---------------------------------------

    raw = (

        uniqueness * 0.25 +

        token_score * 0.45 +

        length_score * 0.30

    )

    stability = (
        1
        /
        (
            1
            +
            math.exp(
                -(raw * 6 - 3)
            )
        )
    )

    return round(
        max(
            0.0,
            min(stability, 1.0)
        ),
        3
  )
