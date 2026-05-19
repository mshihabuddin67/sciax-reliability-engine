from core.response_builder import (
    build_response as legacy_build_response,
    build_structured_response
)

from core.normalization import normalize_text


@app.post("/analyze")
def analyze(input: InputModel):

    normalized_text = normalize_text(input.text)

    variants = perturb(normalized_text)[:3]

    # FIXED
    outputs = [
        v for v in variants
    ]

    metrics = compute_metrics(outputs)

    cs = compute_conflict(outputs)

    risk = risk_analyzer(metrics, cs)

    # Legacy fallback response
    old_result = legacy_build_response(
        input.text,
        metrics,
        cs,
        risk
    )

    try:

        structured_response = build_structured_response(

            input_text=input.text,

            normalized_text=normalized_text,

            risk_level=risk.get("risk_level", "Unknown"),

            raw_confidence=risk.get("confidence_score", 0.5),

            stability_score=metrics.get("stability_score", 0.5),

            conflict_score=cs
        )

        return structured_response

    except Exception as e:

        print("S-CIAX fallback triggered:", e)

        return old_result
