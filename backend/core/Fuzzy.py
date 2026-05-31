# ==================================================
# S-CIAX FUZZY MATCHING LAYER
# ==================================================

from difflib import SequenceMatcher


def similarity(a: str, b: str) -> float:
    """
    Returns similarity score between two strings
    """
    return SequenceMatcher(None, a, b).ratio()


def best_fuzzy_match(text: str, patterns: list, threshold: float = 0.82):
    """
    Finds best fuzzy match from pattern list

    Args:
        text (str): normalized input text
        patterns (list): list of known patterns
        threshold (float): minimum similarity required

    Returns:
        (match, score) or (None, best_score)
    """

    best_match = None
    best_score = 0.0

    for pattern in patterns:

        score = similarity(text, pattern)

        if score > best_score:
            best_score = score
            best_match = pattern

    if best_score >= threshold:
        return best_match, round(best_score, 2)

    return None, round(best_score, 2)
