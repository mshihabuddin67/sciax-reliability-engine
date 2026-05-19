from flask import request, jsonify

from core.response_builder import (
    build_response as legacy_build_response,
    build_structured_response
)

from core.normalization import normalize_text


@app.post("/analyze")
def analyze(input):

    print("\n========== S-CIAX REQUEST START ==========")

    print("[INPUT]", input.text)

    # 1. Normalize
    normalized_text = normalize_text(input.text)
    print("[NORMALIZED]", normalized_text)

    # 2. Variants
    variants = perturb(normalized_text)[:3]
    print("[VARIANTS]", variants)

    # 3. Outputs
    outputs = [v for v in variants]
    print("[OUTPUTS]", outputs)

    # 4. Metrics
    metrics = compute_metrics(outputs)
    print("[METRICS]", metrics)

    # 5. Conflict score
    cs = compute_conflict(outputs)
    print("[CONFLICT]", cs)

    # 6. Risk
    risk = risk_analyzer(metrics, cs)
    print("[RISK]", risk)

    # ==============================
    # LEGACY RESPONSE (FALLBACK)
    # ==============================
    old_result = legacy_build_response(
        input.text,
        metrics,
        cs,
        risk
    )

    try:
        print("[PIPELINE] NEW STRUCTURED ENGINE CALLED")

        structured_response = build_structured_response(

            input_text=input.text,
            normalized_text=normalized_text,

            risk_level=risk.get("risk_level", "Unknown"),

            raw_confidence=risk.get("confidence_score", 0.5),

            stability_score=metrics.get("stability_score", 0.5),

            conflict_score=cs
        )

        print("[PIPELINE] SUCCESS - STRUCTURED RESPONSE RETURNED")
        print("========== S-CIAX REQUEST END ==========\n")

        return jsonify(structured_response)

    except Exception as e:

        print("[PIPELINE ERROR]", str(e))
        print("[PIPELINE] FALLBACK ACTIVATED")
        print("========== S-CIAX REQUEST END ==========\n")

        return jsonify(old_result)
