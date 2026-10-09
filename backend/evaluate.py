import json
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime, timezone

from backend.core.engine import sciax_engine


# ============================================================
# S-CIAX Comprehensive Benchmark Runner V1
#
# Purpose:
#   - Preserve the existing sciax_engine interface.
#   - Evaluate resolved intent and risk separately.
#   - Record candidate intent, confidence, stability and evidence.
#   - Protect existing safe-context and mixed-risk regressions.
#   - Continue running when an individual record raises an error.
#
# This runner does NOT modify engine decisions.
# ============================================================


DATASETS = [
    "backend/datasets/safe.json",
    "backend/datasets/violence.json",
    "backend/datasets/cyber.json",
    "backend/datasets/fraud.json",
    "backend/datasets/edge_cases.json",
]

REPORT_DIR = Path("backend/reports")

# Keep this list aligned with the project's actual intent taxonomy.
# Only use it for FP/FN categorization, not for changing predictions.
HARMFUL_INTENTS = {
    "violent_threat",
    "cyber_intrusion",
    "fraud",
    "social_engineering",
    "credential_theft",
    "harassment",
    "coercion",
}

BENIGN_INTENTS = {
    "non-malicious",
    "unknown_or_safe",
}


def load_json(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def save_json(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            indent=2,
            ensure_ascii=False,
            default=str,
        )


def first_or_none(value):
    """Safely extract the first candidate intent."""
    if isinstance(value, list):
        return value[0] if value else None
    if isinstance(value, str):
        return value
    return None


def get_number(mapping, key):
    """Return a numeric score, or None if unavailable/invalid."""
    if not isinstance(mapping, dict):
        return None

    value = mapping.get(key)

    if isinstance(value, bool):
        return None

    if isinstance(value, (int, float)):
        return value

    return None


def valid_score(value):
    """Scores are expected to be within [0, 1]."""
    return (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and 0.0 <= value <= 1.0
    )


def classify_intent_error(expected, predicted):
    """
    Categorize errors only when the expected/predicted classes
    support a defensible harmful-vs-benign interpretation.
    """
    if expected in HARMFUL_INTENTS and predicted not in HARMFUL_INTENTS:
        return "false_negative"

    if expected not in HARMFUL_INTENTS and predicted in HARMFUL_INTENTS:
        if expected in BENIGN_INTENTS:
            return "false_positive"

    return "other_mismatch"


def evaluate_record(item, dataset_path, index):
    text = item.get("input", "")
    expected_intent = item.get("expected_intent")
    expected_risk = item.get("expected_risk")

    record = {
        "dataset": dataset_path,
        "index": index,
        "input": text,
        "expected_intent": expected_intent,
        "expected_risk": expected_risk,
        "status": "FAIL",
        "errors": [],
    }

    if not isinstance(text, str) or not text.strip():
        record["errors"].append("invalid_or_empty_input")
        record["status"] = "ERROR"
        return record

    try:
        output = sciax_engine(text)

        if not isinstance(output, dict):
            record["errors"].append("engine_output_not_a_dictionary")
            record["status"] = "ERROR"
            return record

        # Candidate and resolved intents have different meanings.
        candidate_intent = first_or_none(
            output.get("intent_classification")
        )
        resolved_intent = output.get("resolved_intent")

        analysis = output.get("analysis", {})
        evidence = output.get("evidence", {})

        if not isinstance(analysis, dict):
            analysis = {}

        if not isinstance(evidence, dict):
            evidence = {}

        record.update({
            "candidate_intent": candidate_intent,
            "resolved_intent": resolved_intent,
            "intent_match": (
                resolved_intent == expected_intent
                if expected_intent is not None
                and resolved_intent is not None
                else None
            ),
            "candidate_match": (
                candidate_intent == expected_intent
                if expected_intent is not None
                and candidate_intent is not None
                else None
            ),
            "predicted_risk": analysis.get("risk_level"),
            "risk_match": (
                analysis.get("risk_level") == expected_risk
                if expected_risk is not None
                and analysis.get("risk_level") is not None
                else None
            ),
            "stability_score": get_number(
                analysis, "stability_score"
            ),
            "confidence_score": get_number(
                analysis, "confidence_score"
            ),
            "intent_consistency": get_number(
                analysis, "intent_consistency"
            ),
            "uncertainty_score": get_number(
                analysis, "uncertainty_score"
            ),
            "evidence_summary": {
                "selected_intent": evidence.get("selected_intent"),
                "selected_intent_score": evidence.get(
                    "selected_intent_score"
                ),
                "global_evidence_quality": evidence.get(
                    "global_evidence_quality"
                ),
                "contradiction_score": evidence.get(
                    "contradiction_score"
                ),
                "evidence_count": evidence.get("evidence_count"),
            },
        })

        # Check whether the expected fields are available.
        if expected_intent is None:
            record["errors"].append("dataset_missing_expected_intent")
        elif resolved_intent is None:
            record["errors"].append("engine_missing_resolved_intent")

        if expected_risk is not None and analysis.get("risk_level") is None:
            record["errors"].append("engine_missing_risk_level")

        # Score validation is informational; it does not silently
        # replace or recalibrate the engine's score.
        score_values = {
            "stability_score": record["stability_score"],
            "confidence_score": record["confidence_score"],
            "intent_consistency": record["intent_consistency"],
            "uncertainty_score": record["uncertainty_score"],
        }

        record["score_validation"] = {
            name: (
                "PASS" if valid_score(value)
                else "MISSING_OR_INVALID"
            )
            for name, value in score_values.items()
        }

        # Check confidence/uncertainty consistency only when both
        # scores exist. Current engine may round uncertainty.
        confidence = record["confidence_score"]
        uncertainty = record["uncertainty_score"]

        if confidence is not None and uncertainty is not None:
            record["confidence_uncertainty_consistent"] = (
                abs((confidence + uncertainty) - 1.0) <= 0.02
            )
        else:
            record["confidence_uncertainty_consistent"] = None

        intent_ok = record["intent_match"] is True
        risk_ok = (
            record["risk_match"] is True
            if expected_risk is not None
            else True
        )

        missing_required_output = any(
            error in record["errors"]
            for error in (
                "dataset_missing_expected_intent",
                "engine_missing_resolved_intent",
                "engine_missing_risk_level",
            )
        )

        record["status"] = (
            "PASS"
            if intent_ok and risk_ok and not missing_required_output
            else "FAIL"
        )

        if record["intent_match"] is False:
            record["intent_error_type"] = classify_intent_error(
                expected_intent,
                resolved_intent,
            )

        # Include the complete evidence structure in the detailed
        # report for debugging. Do not use it as a final decision.
        record["evidence_detail"] = evidence

        return record

    except Exception as exc:
        record["status"] = "ERROR"
        record["errors"].append(
            f"{type(exc).__name__}: {str(exc)}"
        )
        return record


def build_confusion_matrix(results):
    """Resolved-intent confusion matrix for records with valid labels."""
    matrix = defaultdict(Counter)

    for record in results:
        expected = record.get("expected_intent")
        predicted = record.get("resolved_intent")

        if expected is None or predicted is None:
            continue

        matrix[expected][predicted] += 1

    return {
        expected: dict(predictions)
        for expected, predictions in sorted(matrix.items())
    }


def evaluate():
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    results = []
    dataset_summary = {}
    missing_datasets = []

    for dataset_path in DATASETS:
        path = Path(dataset_path)

        if not path.exists():
            missing_datasets.append(dataset_path)
            dataset_summary[dataset_path] = {
                "status": "MISSING_DATASET",
                "records": 0,
            }
            continue

        try:
            dataset = load_json(path)

            if not isinstance(dataset, list):
                raise ValueError("Dataset root must be a JSON list.")

        except Exception as exc:
            missing_datasets.append(dataset_path)
            dataset_summary[dataset_path] = {
                "status": "DATASET_LOAD_ERROR",
                "error": f"{type(exc).__name__}: {str(exc)}",
                "records": 0,
            }
            continue

        print(f"Loaded {len(dataset)} records from {dataset_path}")

        dataset_results = []

        for index, item in enumerate(dataset, start=1):
            if not isinstance(item, dict):
                record = {
                    "dataset": dataset_path,
                    "index": index,
                    "status": "ERROR",
                    "errors": ["dataset_record_not_a_dictionary"],
                }
            else:
                record = evaluate_record(item, dataset_path, index)

            results.append(record)
            dataset_results.append(record)

        passed = sum(r["status"] == "PASS" for r in dataset_results)
        failed = sum(r["status"] == "FAIL" for r in dataset_results)
        errors = sum(r["status"] == "ERROR" for r in dataset_results)

        dataset_summary[dataset_path] = {
            "status": "COMPLETED",
            "records": len(dataset_results),
            "passed": passed,
            "failed": failed,
            "errors": errors,
            "pass_rate": round(passed / len(dataset_results), 4)
            if dataset_results else None,
        }

    passed = sum(r.get("status") == "PASS" for r in results)
    failed = sum(r.get("status") == "FAIL" for r in results)
    errors = sum(r.get("status") == "ERROR" for r in results)
    total = len(results)

    intent_mismatches = [
        r for r in results
        if r.get("intent_match") is False
    ]

    risk_mismatches = [
        r for r in results
        if r.get("risk_match") is False
    ]

    false_negatives = [
        r for r in intent_mismatches
        if r.get("intent_error_type") == "false_negative"
    ]

    false_positives = [
        r for r in intent_mismatches
        if r.get("intent_error_type") == "false_positive"
    ]

    other_mismatches = [
        r for r in intent_mismatches
        if r.get("intent_error_type") == "other_mismatch"
    ]

    exception_records = [
        r for r in results
        if r.get("status") == "ERROR"
    ]

    summary = {
        "benchmark_version": "comprehensive_v1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "total_records": total,
        "passed": passed,
        "failed": failed,
        "errors": errors,
        "pass_rate": round(passed / total, 4) if total else None,
        "intent_mismatches": len(intent_mismatches),
        "risk_mismatches": len(risk_mismatches),
        "false_negatives": len(false_negatives),
        "false_positives": len(false_positives),
        "other_intent_mismatches": len(other_mismatches),
        "missing_datasets": missing_datasets,
        "dataset_summary": dataset_summary,
        "resolved_intent_confusion_matrix": build_confusion_matrix(results),
        "notes": [
            "Final intent is evaluated using resolved_intent.",
            "candidate_match is informational, not the final intent score.",
            "Risk is evaluated only when expected_risk exists in the dataset.",
            "Missing datasets are reported and are not counted as test records.",
            "Recommended action is not tested because the current engine response "
            "does not expose that field.",
            "A passing score does not establish production readiness.",
        ],
    }

    save_json(REPORT_DIR / "benchmark_results.json", results)
    save_json(REPORT_DIR / "benchmark_summary.json", summary)
    save_json(REPORT_DIR / "intent_mismatches.json", intent_mismatches)
    save_json(REPORT_DIR / "risk_mismatches.json", risk_mismatches)
    save_json(REPORT_DIR / "false_negatives.json", false_negatives)
    save_json(REPORT_DIR / "false_positives.json", false_positives)
    save_json(REPORT_DIR / "other_intent_mismatches.json", other_mismatches)
    save_json(REPORT_DIR / "benchmark_errors.json", exception_records)

    print("\n========== S-CIAX BENCHMARK SUMMARY ==========")
    print(f"Total records:       {total}")
    print(f"PASS:                {passed}")
    print(f"FAIL:                {failed}")
    print(f"ERROR:               {errors}")
    print(f"Intent mismatches:   {len(intent_mismatches)}")
    print(f"Risk mismatches:     {len(risk_mismatches)}")
    print(f"False negatives:     {len(false_negatives)}")
    print(f"False positives:     {len(false_positives)}")
    print(f"Missing datasets:    {len(missing_datasets)}")
    print(f"Pass rate:           {summary['pass_rate']}")
    print(f"Reports directory:   {REPORT_DIR}")

    if missing_datasets:
        print("\nWARNING: Some datasets were missing or could not be loaded.")
        for dataset in missing_datasets:
            print(f"  - {dataset}")

    print("==============================================")

    return summary


if __name__ == "__main__":
    evaluate()

