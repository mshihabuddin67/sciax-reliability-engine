def compute_stability_score(variants):
    base = variants[0].lower()

    matches = 0
    for v in variants:
        if v.lower() == base:
            matches += 1

    return round(matches / len(variants), 2)
