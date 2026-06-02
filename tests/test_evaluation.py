import json
from backend.core.sciax_engine import sciax_engine


# ==================================================
# LOAD DATASET
# ==================================================

DATASET_PATH = "datasets/sciax_eval.json"


def load_dataset():
    with open(DATASET_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


# ==================================================
# METRICS TRACKER
# ==================================================

def evaluate():

    data = load_dataset()

    total = len(data)

    correct_intent = 0
    correct_risk = 0

    intent_confusion = {}
    risk_confusion = {}

    for item in data:

        result = sciax_engine(item["input"])

        predicted_intent = result.get("intent", "unknown")
        predicted_risk = result["analysis"]["risk_level"]

        expected_intent = item["expected_intent"]
        expected_risk = item["expected_risk"]

        # -----------------------------
        # INTENT ACCURACY
        # -----------------------------
        if predicted_intent == expected_intent:
            correct_intent += 1

        intent_confusion.setdefault(expected_intent, {})
        intent_confusion[expected_intent].setdefault(predicted_intent, 0)
        intent_confusion[expected_intent][predicted_intent] += 1

        # -----------------------------
        # RISK ACCURACY
        # -----------------------------
        if predicted_risk == expected_risk:
            correct_risk += 1

        risk_confusion.setdefault(expected_risk, {})
        risk_confusion[expected_risk].setdefault(predicted_risk, 0)
        risk_confusion[expected_risk][predicted_risk] += 1

    # ==================================================
    # FINAL METRICS
    # ==================================================

    intent_accuracy = correct_intent / total
    risk_accuracy = correct_risk / total

    report = {
        "total_samples": total,
        "intent_accuracy": round(intent_accuracy, 3),
        "risk_accuracy": round(risk_accuracy, 3),
        "intent_confusion_matrix": intent_confusion,
        "risk_confusion_matrix": risk_confusion
    }

    return report


# ==================================================
# RUN TEST
# ==================================================

if __name__ == "__main__":

    result = evaluate()

    print("\n===== S-CIAX EVALUATION REPORT =====\n")
    print(json.dumps(result, indent=2, ensure_ascii=False))
