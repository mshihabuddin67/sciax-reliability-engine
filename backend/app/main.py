from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

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
# ROOT
# ----------------------------
@app.get("/")
def root():
    return {
        "status": "S-CIAX Running",
        "version": "1.1.0"
    }

# ----------------------------
# ANALYZE
# ----------------------------
@app.post("/analyze")
def analyze(input: InputModel, x_api_key: str = Header(None)):

    verify_key(x_api_key)

    text = input.text.lower()

    # Defaults
    stability_score = DEFAULT_STABILITY
    conflict_score = DEFAULT_CONFLICT
    risk_level = DEFAULT_RISK
    reason = "Normal stable interaction detected"

    # ----------------------------
    # MULTILINGUAL DETECTION
    # ----------------------------
    for category, words in MULTI_LANG_RISK.items():

        for w in words:

            if w.lower() in text:

                risk_level = "High"
                stability_score = 0.3
                conflict_score = 0.8
                reason = f"Multilingual signal detected ({category})"

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
