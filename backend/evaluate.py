import json
from backend.core.sciax_engine import sciax_engine

DATASETS = [
"datasets/safe.json",
"datasets/violence.json",
"datasets/cyber.json",
"datasets/fraud.json",
"datasets/edge_cases.json",
]

def load_json(path):
with open(path, "r", encoding="utf-8") as f:
return json.load(f)

def save(path, data):
with open(path, "w", encoding="utf-8") as f:
json.dump(data, f, indent=2)

def evaluate():

results = []
false_negatives = []

for file in DATASETS:

    data = load_json(file)

    print(f"Loaded {len(data)} records from {file}")

    for item in data:

        output = sciax_engine(item["input"])

        # FIX: use intent, not risk_level
        predicted_intent = output["intent_classification"][0]

        expected_intent = item["expected_intent"]

        status = (
            "PASS"
            if predicted_intent == expected_intent
            else "FAIL"
        )

        record = {
            "input": item["input"],
            "expected": expected_intent,
            "predicted": predicted_intent,
            "status": status
        }

        results.append(record)

        if status == "FAIL":
            false_negatives.append(record)

save(
    "backend/reports/benchmark_results.json",
    results
)

save(
    "backend/reports/false_negatives.json",
    false_negatives
)

print(f"Benchmark records saved: {len(results)}")
print(f"Failures: {len(false_negatives)}")

if name == "main":
evaluate()
