from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rapidfuzz import fuzz
import re

from backend.app.config import (
    API_KEYS,
    DEFAULT_STABILITY,
    DEFAULT_CONFLICT,
    DEFAULT_RISK,
    MULTI_LANG_RISK
)

# NEW HYBRID IMPORTS
from core.normalization import normalize_text
from core.engine import sciax_engine
from core.behavioral_signals import detect_behavioral_signals
from core.intent_engine import classify_intent
from core.language_profiles import detect_language_profile
from core.explainability import generate_explanations
from core.response_builder import build_response


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class InputModel(BaseModel):
    text: str


def verify_key(api_key: str):

    if not api_key:
        raise HTTPException(status_code=401, detail="API key missing")

    if api_key not in API_KEYS:
        raise HTTPException(status_code=403, detail="Invalid API key")


def detect_language_safe(text: str) -> str:

    has_bangla = bool(re.search(r'[\u0980-\u09FF]', text))
    has_hindi = bool(re.search(r'[\u0900-\u097F]', text))

    return "mixed_or_non_latin" if (has_bangla or has_hindi) else "latin"


@app.get("/")
def root():
    return {
        "status": "S-CIAX Hybrid Engine Running",
        "version": "9.0.0"
    }


@app.post("/analyze")
def analyze(input: InputModel, x_api_key: str = Header(None)):

    verify_key(x_api_key)

    original_text = input.text

    # =====================================
    # LANGUAGE + NORMALIZATION
    # =====================================
    language_type = detect_language_safe(original_text)
    normalized_text = normalize_text(original_text)

    # =====================================
    # HYBRID ENGINE LAYER
    # =====================================
    engine_output = sciax_engine(normalized_text)

    # =====================================
    # INTELLIGENCE LAYERS
    # =====================================
    behavioral = detect_behavioral_signals(normalized_text)
    intent = classify_intent(normalized_text)
    language = detect_language_profile(original_text)
    explainability = generate_explanations(normalized_text)

    # =====================================
    # FINAL HYBRID RESPONSE BUILDER
    # =====================================
    response = build_response(
        input_text=original_text,
        engine_output=engine_output,
        behavioral_signals=behavioral,
        intent_classification=intent,
        language_profile=language,
        explainability=explainability
    )

    return response
