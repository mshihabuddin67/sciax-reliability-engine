from flask import Blueprint, jsonify

from core.response_builder import build_response
from core.normalization import normalize_text

# Existing imports
# Keep your existing imports below if already present
# from utils.xxx import ...
# from models.xxx import ...
# etc.


analyze_route = Blueprint("analyze", __name__)


@analyze_route.post("/analyze")
def analyze(input):

    print("\n========== S-CIAX REQUEST START ==========")

    print("[INPUT]", input.text)

    # =====================================
    # 1. Normalize
    # =====================================
    normalized_text = normalize_text(input.text)

    print("[NORMALIZED]", normalized_text)

    # =====================================
    # 2. Generate Variants
    # =====================================
    variants = perturb(normalized_text)[:3]

    print("[VARIANTS]", variants)

    # =====================================
    # 3. Outputs
    # =====================================
    outputs = [v for v in variants]

    print("[OUTPUTS]", outputs)

    # =====================================
    # 4. Metrics
    # =====================================
    metrics = compute_metrics(outputs)

    print("[METRICS]", metrics)
    print("[METRICS TYPE]", type(metrics))

    # =====================================
    # 5. Conflict Score
    # =====================================
    cs = compute_conflict(outputs)

    print("[CONFLICT]", cs)

    # =====================================
    # 6. Risk Analysis
    # =====================================
    risk = risk_analyzer(metrics, cs)

    print("[RISK]", risk)
    print("[RISK TYPE]", type(risk))

    # =====================================
    # SAFE BACKWARD-COMPATIBILITY HANDLING
    # =====================================

    # Risk Level
    if isinstance(risk, dict):
        risk_level = risk.get(
            "risk_level",
            "Unknown"
        )

        raw_confidence = risk.get(
            "confidence_score",
            0.85
        )

    else:
        risk_level = str(risk)
        raw_confidence = 0.85

    # Stability Score
    if isinstance(metrics, dict):

        stability_score = metrics.get(
            "stability_score",
            0.5
        )

    else:
        stability_score = 0.5

    # =====================================
    # Structured Response
    # =====================================

    structured_response = build_response(

        input_text=input.text,

        normalized_text=normalized_text,

        risk_level=risk_level,

        raw_confidence=raw_confidence,

        stability_score=stability_score,

        conflict_score=cs
    )

    print("[PIPELINE] STRUCTURED RESPONSE ACTIVE")

    print(
        "========== S-CIAX REQUEST END ==========\n"
    )

    return jsonify(structured_response)
