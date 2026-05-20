from flask import request, jsonify

from core.response_builder import build_response
from core.normalization import normalize_text


@app.post("/analyze")
def analyze(input):

    print("\n========== S-CIAX REQUEST START ==========")

    print("[INPUT]", input.text)

    normalized_text = normalize_text(input.text)
    print("[NORMALIZED]", normalized_text)

    variants = perturb(normalized_text)[:3]
    print("[VARIANTS]", variants)

    outputs = [v for v in variants]

    metrics = compute_metrics(outputs)
    print("[METRICS]", metrics)

    cs = compute_conflict(outputs)
    print("[CONFLICT]", cs)

    risk = risk_analyzer(metrics, cs)
    print("[RISK]", risk)

    structured_response = build_response(

        input_text=input.text,

        normalized_text=normalized_text,

        risk_level=risk.get("risk_level", "Unknown"),

        raw_confidence=risk.get("confidence_score", 0.5),

        stability_score=metrics.get(
            "stability_score",
            0.5
        ),

        conflict_score=cs
    )

    print("[PIPELINE] STRUCTURED RESPONSE ACTIVE")
    print("========== S-CIAX REQUEST END ==========\n")

    return jsonify(structured_response)
