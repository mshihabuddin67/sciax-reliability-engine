from collections import Counter

from backend.core.intent_engine import classify_intent


def compute_intent_consistency(variants):
    """
    Intent Consistency Engine V3

    Measures how consistently the same
    intent is detected across variants.
    """

    if not variants:
        return 0.0

    predictions = []

    for variant in variants:

        intents = classify_intent(variant)

        if intents:
            predictions.append(intents[0])

    if not predictions:
        return 0.0

    counts = Counter(predictions)

    score = max(counts.values()) / len(predictions)

    return round(score, 3)
