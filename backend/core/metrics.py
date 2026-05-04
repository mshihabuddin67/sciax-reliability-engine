def compute_stability_score(variants):
    """
    Simple similarity-based stability approximation
    (upgradeable to embeddings later)
    """

    base = len(set(variants))
    total = len(variants)

    stability = 1 - (base - 1) / total

    return round(max(0.0, min(1.0, stability)), 2)
