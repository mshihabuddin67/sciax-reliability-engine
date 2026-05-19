def calibrate_confidence(raw_score):

    if raw_score >= 1:
        return 0.96

    if raw_score > 0.97:
        return 0.97

    return round(raw_score, 2)


def calculate_uncertainty(confidence):

    return round(1 - confidence, 2)
