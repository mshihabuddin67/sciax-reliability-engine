from fastapi import APIRouter
from pydantic import BaseModel

from backend.core.normalization import normalize_text
from backend.core.engine import sciax_engine
from backend.core.behavioral_signals import detect_behavioral_signals
from backend.core.intent_engine import classify_intent
from backend.core.language_profiles import detect_language_profile
from backend.core.explainability import generate_explanations
from backend.app.response import build_response


analyze_route = APIRouter()


class InputModel(BaseModel):
    text: str


@analyze_route.post("/analyze")
def analyze(input: InputModel):

    print("\n========== S-CIAX REQUEST START ==========")
    print("[INPUT]", input.text)

    # 1. Normalize
    normalized = normalize_text(input.text)
    print("[NORMALIZED]", normalized)

    # 2. Engine
    engine_output = sciax_engine(normalized)
    print("[ENGINE OUTPUT]", engine_output)

    # 3. Behavioral signals
    behavioral = detect_behavioral_signals(normalized)
    print("[BEHAVIORAL]", behavioral)

    # 4. Intent classification
    intent = classify_intent(normalized)
    print("[INTENT]", intent)

    # 5. Language detection
    language = detect_language_profile(input.text)
    print("[LANGUAGE]", language)

    # 6. Explainability
    explainability = generate_explanations(
        text=normalized,
        intents=intent,
        behavioral_signals=behavioral
    )
    print("[EXPLAINABILITY]", explainability)

    # 7. Final response
    response = build_response(
        input_text=input.text,
        engine_output=engine_output,
        behavioral_signals=behavioral,
        intent_classification=intent,
        language_profile=language,
        explainability=explainability
    )

    print("[PIPELINE] RESPONSE READY")
    print("========== S-CIAX REQUEST END ==========\n")

    return response
