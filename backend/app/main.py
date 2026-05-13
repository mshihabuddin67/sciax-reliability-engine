from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.app.config import (
    API_KEYS,
    DEFAULT_STABILITY,
    DEFAULT_CONFLICT,
    DEFAULT_RISK,
    HIGH_RISK_THRESHOLD,
    MEDIUM_RISK_THRESHOLD,
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
# AUTH CHECK
# ----------------------------
def verify_key(api_key: str):

    if not api_key:
        raise HTTPException(status_code=401, detail="API key missing")

    if api_key not in API_KEYS:
        raise HTTPException(status_code=403, detail="Invalid API key")

# ----------------------------
# ROOT
# ----------------------------
@app.get("/")
def root():
    return {
        "status": "S-CIAX Engine Running",
        "version": "1.1.0"
    }

# ----------------------------
# ANALYZE ENGINE
# ----------------------------
@app.post("/analyze")
def analyze(input: InputModel, x_api_key: str = Header(None)):

    verify_key(x_api_key)

    text = input.text.lower()

    # ----------------------------
    # DEFAULTS
    # ----------------------------
    stability_score = DEFAULT_STABILITY
    conflict_score = DEFAULT_CONFLICT
    risk_level = DEFAULT_RISK
    reason = "Normal stable interaction detected"

    # ----------------------------
    # HIGH RISK
    # ----------------------------
    high_risk_words = [
        "hack", "attack", "exploit",
        "bypass", "fraud", "steal",
        "destroy", "malware"
    ]

    for word in high_risk_words:

        if word in text:

            risk_level = "High"
            stability_score = 0.3
            conflict_score = 0.8
            reason = "Detected exploit or attack-related terminology"

    # ----------------------------
    # MEDIUM RISK
    # ----------------------------
    if risk_level != "High":

        medium_risk_words = [
            "refund", "angry", "problem",
            "report", "complaint", "error",
            "broken"
        ]

        for word in medium_risk_words:

            if word in text:

                risk_level = "Medium"
                stability_score = 0.6
                conflict_score = 0.5
                reason = "Detected complaint or unstable interaction pattern"

    # ----------------------------
    # MULTILINGUAL LAYER
    # ----------------------------
    for category, words in MULTI_LANG_RISK.items():

        for w in words:

            if w.lower() in text:

                risk_level = "High"
                stability_score = 0.3
                conflict_score = 0.8
                reason = f"Multilingual signal detected ({category})"

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
        "input": input.text,
        "risk_level": risk_level,
        "stability_score": round(stability_score, 2),
        "conflict_score": round(conflict_score, 2),
        "reason": reason
        }
