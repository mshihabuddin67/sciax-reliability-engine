from flask import Blueprint, jsonify

from core.normalization import normalize_text
from core.engine import sciax_engine

from core.behavioral_signals import detect_behavioral_signals
from core.intent_engine import classify_intent
from core.language_profiles import detect_language_profile
from core.explainability import generate_explanations

from core.response_builder import build_response

# Existing imports (keep yours if needed)
# from core.metrics import compute_metrics
# from core.risk import risk_analyzer
# from core.perturbation import perturb


analyze_route = Blueprint("analyze", __name__)


@analyze_route.post("/analyze")
def analyze(input):

    print("\n========== S-CIAX REQUEST START ==========")

    text = input.text
    print("[INPUT]", text)

    # =====================================
    # 1. Normalize
    # =====================================
    normalized = normalize_text(text)
    print("[NORMALIZED]", normalized)

    # =====================================
    # 2. Engine (signal generator)
    # =====================================
    engine_output = sciax_engine(normalized)
    print("[ENGINE OUTPUT]", engine_output)

    # =====================================
    # 3. Intelligence Layer
    # =====================================
    behavioral = detect_behavioral_signals(normalized)
    intent = classify_intent(normalized)
    language = detect_language_profile(text)
    explainability = generate_explanations(normalized)

    print("[BEHAVIOR]", behavioral)
    print("[INTENT]", intent)
    print("[LANG]", language)

    # =====================================
    # 4. Structured Response (HYBRID BRAIN)
    # =====================================
    response = build_response(
        input_text=text,
        engine_output=engine_output,
        behavioral_signals=behavioral,
        intent_classification=intent,
        language_profile=language,
        explainability=explainability
    )

    print("[PIPELINE] HYBRID RESPONSE GENERATED")
    print("========== S-CIAX REQUEST END ==========\n")

    return jsonify(response)
