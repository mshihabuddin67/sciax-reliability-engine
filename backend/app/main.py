from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rapidfuzz import fuzz

from backend.app.config import (
    API_KEYS,
    DEFAULT_STABILITY,
    DEFAULT_CONFLICT,
    DEFAULT_RISK,
    MULTI_LANG_RISK
)

app = FastAPI()

# ----------------------------
# CORS
# ----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------
# INPUT MODEL
# ----------------------------
class InputModel(BaseModel):
    text: str

# ----------------------------
# AUTH
# ----------------------------
def verify_key(api_key: str):

    if not api_key:
        raise HTTPException(status_code=401, detail="API key missing")

    if api_key not in API_KEYS:
        raise HTTPException(status_code=403, detail="Invalid API key")

# ----------------------------
# NORMALIZATION LAYER
# ----------------------------
def normalize_text(text):

    replacements = {

        # Banglish / Hinglish variations
        "haek": "hack",
        "hek": "hack",
        "hyack": "hack",

        "bypass korbo": "bypass",
        "system bhangbo": "destroy system",

        "attack korbo": "attack",
        "hamla": "attack",

        "churi": "steal",
        "data churi": "steal data",

        "dhongsho": "destroy",
        "borbad": "destroy",

        "hax": "hack"
    }

    normalized = text.lower()

    for wrong, correct in replacements.items():

        normalized = normalized.replace(wrong, correct)

    return normalized

# ----------------------------
# ROOT
# ----------------------------
@app.get("/")
def root():

    return {
        "status": "S-CIAX Running",
        "version": "3.0.0"
    }

# ----------------------------
# ANALYZE
# ----------------------------
@app.post("/analyze")
def analyze(input: InputModel, x_api_key: str = Header(None)):

    verify_key(x_api_key)

    original_text = input.text

    # ----------------------------
    # NORMALIZED TEXT
    # ----------------------------
    text = normalize_text(original_text)

    # ----------------------------
    # DEFAULTS
    # ----------------------------
    stability_score = DEFAULT_STABILITY
    conflict_score = DEFAULT_CONFLICT
    risk_level = DEFAULT_RISK

    reason = "Normal stable interaction detected"

    # ----------------------------
    # SEMANTIC PATTERNS
    # ----------------------------
    semantic_patterns = [

        "hack the system",
        "bypass security",
        "steal data",
        "destroy system",
        "attack server",
        "exploit vulnerability",

        "kill everyone",
        "burn the house"
    ]

    # ----------------------------
    # SEMANTIC SIMILARITY
    # ----------------------------
    for pattern in semantic_patterns:

        similarity = fuzz.partial_ratio(text, pattern)

        if similarity > 80:

            risk_level = "High"

            stability_score = 0.35
            conflict_score = 0.75

            reason = (
                f"Semantic similarity matched risky intent "
                f"({pattern}) score={similarity}"
            )

    # ----------------------------
    # MULTILINGUAL LAYER
    # ----------------------------
    for category, words in MULTI_LANG_RISK.items():

        for w in words:

            if w.lower() in text:

                risk_level = "High"

                stability_score = 0.3
                conflict_score = 0.8

                reason = (
                    f"Multilingual risky signal detected "
                    f"({category})"
                )

    # ----------------------------
    # MEDIUM RISK
    # ----------------------------
    medium_risk_words = [

        "problem",
        "broken",
        "complaint",
        "refund",
        "angry",
        "issue",
        "error",
        "bad service",
        "not working",

        "rag",
        "kharap",
        "somossa",

        "gussa",
        "samasya"
    ]

    if risk_level != "High":

        for word in medium_risk_words:

            if word in text:

                risk_level = "Medium"

                stability_score = 0.6
                conflict_score = 0.5

                reason = (
                    "Detected unstable or complaint-related interaction"
                )

    # ----------------------------
    # LENGTH EFFECT
    # ----------------------------
    if len(text) > 120:

        stability_score -= 0.1
        conflict_score += 0.1

    # ----------------------------
    # CLAMP
    # ----------------------------
    stability_score = max(0.1, min(1.0, stability_score))
    conflict_score = max(0.0, min(1.0, conflict_score))

    # ----------------------------
    # RESPONSE
    # ----------------------------
    return {

        "input": original_text,

        "normalized_text": text,

        "risk_level": risk_level,

        "stability_score": round(stability_score, 2),

        "conflict_score": round(conflict_score, 2),

        "reason": reason
    }
