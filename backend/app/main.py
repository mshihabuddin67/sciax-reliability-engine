from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# --------------------------------
# CORS FIX
# --------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------
# Request Model
# --------------------------------
class InputModel(BaseModel):
    text: str

# --------------------------------
# Root Endpoint
# --------------------------------
@app.get("/")
def root():
    return {"status": "running"}

# --------------------------------
# S-CIAX Smart Analyze Endpoint
# --------------------------------
@app.post("/analyze")
def analyze(input: InputModel):

    text = input.text
    text_lower = text.lower()

    # ----------------------------
    # Default Scores
    # ----------------------------
    stability_score = 0.9
    conflict_score = 0.1
    risk_level = "Low"
    reason = "Normal stable interaction detected"

    # ----------------------------
    # High Risk Keywords
    # ----------------------------
    high_risk_words = [
        "hack",
        "attack",
        "exploit",
        "bypass",
        "fraud",
        "destroy",
        "steal",
        "malware"
    ]

    # ----------------------------
    # Medium Risk Keywords
    # ----------------------------
    medium_risk_words = [
        "refund",
        "angry",
        "problem",
        "report",
        "complaint",
        "broken",
        "error"
    ]

    # ----------------------------
    # High Risk Detection
    # ----------------------------
    for word in high_risk_words:
        if word in text_lower:
            risk_level = "High"
            stability_score = 0.3
            conflict_score = 0.8
            reason = "Detected exploit or attack-related terminology"

    # ----------------------------
    # Medium Risk Detection
    # ----------------------------
    if risk_level != "High":
        for word in medium_risk_words:
            if word in text_lower:
                risk_level = "Medium"
                stability_score = 0.6
                conflict_score = 0.5
                reason = "Detected complaint or unstable interaction pattern"

    # ----------------------------
    # Length Influence
    # ----------------------------
    length = len(text)

    if length > 120:
        stability_score -= 0.1
        conflict_score += 0.1

    # ----------------------------
    # Clamp values
    # ----------------------------
    stability_score = max(0.1, min(1.0, stability_score))
    conflict_score = max(0.0, min(1.0, conflict_score))

    # ----------------------------
    # Final Response
    # ----------------------------
    return {
        "input": text,
        "risk_level": risk_level,
        "stability_score": round(stability_score, 2),
        "conflict_score": round(conflict_score, 2),
        "reason": reason
    }
