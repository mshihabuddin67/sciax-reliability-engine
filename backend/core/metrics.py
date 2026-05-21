def compute_stability_score(variants):

    """
    Simple lightweight stability scoring
    for Render free-tier compatibility.
    """

    if not variants:
        return 0.5

    unique_variants = len(set(variants))

    total_variants = len(variants)

    diversity_ratio = (
        unique_variants / total_variants
    )

    stability_score = 1 - diversity_ratio

    return round(stability_score, 2)
