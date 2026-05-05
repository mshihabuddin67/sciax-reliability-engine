import random

def compute_metrics(outputs):
    return {
        "SI": round(random.uniform(0.4, 0.9), 2),
        "DI": round(random.uniform(0.1, 0.7), 2),
        "SV": round(random.uniform(0.1, 0.6), 2)
    }

def compute_conflict(outputs):
    return round(random.uniform(0.1, 0.9), 2)
