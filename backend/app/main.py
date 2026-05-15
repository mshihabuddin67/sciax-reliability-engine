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

# --------------------------------------------------
# CORS
# --------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------------------------
# INPUT MODEL
# --------------------------------------------------
class InputModel(BaseModel):
    text: str


# --------------------------------------------------
# API KEY VERIFICATION
# --------------------------------------------------
def verify_key(api_key: str):

    if not api_key:
        raise HTTPException(
            status_code=401,
            detail="API key missing"
        )

    if api_key not in API_KEYS:
        raise HTTPException(
            status_code=403,
            detail="Invalid API key"
        )


# --------------------------------------------------
# NORMALIZATION LAYER
# --------------------------------------------------
def normalize_text(text: str) -> str:
    """
    Lightweight multilingual normalization
    for Bangla + Hindi + English mixed input
    """

    text = text.lower().strip()

    replacements = {

        # hack variations
        "haek": "hack",
        "hek": "hack",
        "hyack": "hack",
        "hax": "hack",

        # destroy variations
        "dhongsho": "destroy",
        "borbad": "destroy",

        # steal variations
        "churi": "steal",
        "data churi": "steal data",

        # attack variations
        "hamla": "attack",

        # system destruction
        "system bhangbo": "destroy system",
        "system bhang": "destroy system",

        # bypass variations
        "bypass korbo": "bypass",
        "bypass kori": "bypass"
    }

    for wrong, correct in replacements.items():

        if wrong in text:
            text = text.replace(wrong, correct)

    # cleanup spaces
    text = " ".join(text.split())

    return text


# --------------------------------------------------
# SAFE CONTEXTS
# --------------------------------------------------
SAFE_CONTEXTS = [

    "sleep schedule",
    "life hack",
    "study hack",
    "productivity hack",

    "game level",
    "video game",
    "gaming strategy",

    "kill time",
    "destroy boredom",

    "football attack",
    "attack strategy in chess"
]


# --------------------------------------------------
# SEMANTIC RISK PATTERNS
# --------------------------------------------------
SEMANTIC_PATTERNS = [

    "hack the system",
    "bypass security",
    "steal data",
    "destroy system",
    "attack server",
    "exploit vulnerability",

    "kill everyone",
    "burn the house"
]


# --------------------------------------------------
# MEDIUM RISK WORDS
# --------------------------------------------------
MEDIUM_RISK_WORDS = [

    "angry",
    "problem",
    "broken",
    "refund",
    "complaint",
    "issue",
    "error",
    "bad service",
    "not working",

    # Banglish
    "rag",
    "kharap",
    "somossa",

    # Hindi
    "gussa",
    "samasya"
]


# --------------------------------------------------
# ROOT
# --------------------------------------------------
@app.get("/")
def root():

    return {
        "status": "S-CIAX Running",
        "version": "5.0.0"
    }


# --------------------------------------------------
# ANALYZE ENGINE
# --------------------------------------------------
@app.post("/analyze")
def analyze(
    input: InputModel,
    x_api_key: str = Header(None)
):

    verify_key(x_api_key)

    original_text = input.text

    # ----------------------------------------------
    # NORMALIZATION
    # ----------------------------------------------
    text = normalize_text(original_text)

    # ----------------------------------------------
    # DEFAULT VALUES
    # ----------------------------------------------
    risk_level = DEFAULT_RISK

    stability_score = DEFAULT_STABILITY
    conflict_score = DEFAULT_CONFLICT

    confidence_score = 0.55

    reason = "Normal stable interaction detected"

    safe_detected = False

    # ----------------------------------------------
    # SAFE CONTEXT CHECK
    # ----------------------------------------------
    for safe in SAFE_CONTEXTS:

        if safe in text:

            safe_detected = True

            risk_level = "Low"

            stability_score = 0.9
            conflict_score = 0.1

            confidence_score = 0.92

            reason = (
                f"Safe context detected ({safe})"
            )

    # ----------------------------------------------
    # SEMANTIC SIMILARITY CHECK
    # ----------------------------------------------
    if not safe_detected:

        for pattern in SEMANTIC_PATTERNS:

            similarity = fuzz.partial_ratio(
                text,
                pattern
            )

            if similarity >= 80:

                risk_level = "High"

                stability_score = 0.3
                conflict_score = 0.8

                confidence_score = round(
                    similarity / 100,
                    2
                )

                reason = (
                    f"Semantic risky intent detected "
                    f"({pattern})"
                )

    # ----------------------------------------------
    # MULTILINGUAL RISK CHECK
    # ----------------------------------------------
    if not safe_detected and risk_level != "High":

        for category, words in MULTI_LANG_RISK.items():

            for word in words:

                if word.lower() in text:

                    risk_level = "High"

                    stability_score = 0.3
                    conflict_score = 0.8

                    confidence_score = 0.89

                    reason = (
                        f"Multilingual risky signal "
                        f"detected ({category})"
                    )

    # ----------------------------------------------
    # MEDIUM RISK CHECK
    # ----------------------------------------------
    if risk_level != "High":

        for word in MEDIUM_RISK_WORDS:

            if word in text:

                risk_level = "Medium"

                stability_score = 0.6
                conflict_score = 0.5

                confidence_score = 0.72

                reason = (
                    "Detected unstable or "
                    "complaint-related interaction"
                )

    # ----------------------------------------------
    # LONG INPUT EFFECT
    # ----------------------------------------------
    if len(text) > 120:

        stability_score -= 0.1
        conflict_score += 0.1

    # ----------------------------------------------
    # VALUE CLAMP
    # ----------------------------------------------
    stability_score = max(
        0.1,
        min(1.0, stability_score)
    )

    conflict_score = max(
        0.0,
        min(1.0, conflict_score)
    )

    confidence_score = max(
        0.0,
        min(1.0, confidence_score)
    )

    # ----------------------------------------------
    # FINAL RESPONSE
    # ----------------------------------------------
    return {

        "input": original_text,

        "normalized_text": text,

        "risk_level": risk_level,

        "confidence_score": round(
            confidence_score,
            2
        ),

        "stability_score": round(
            stability_score,
            2
        ),

        "conflict_score": round(
            conflict_score,
            2
        ),

        "reason": reason
        }
