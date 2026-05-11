from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# ----------------------------
# CORS (IMPORTANT FOR FRONTEND)
# ----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------
# Input Schema
# ----------------------------
class InputModel(BaseModel):
    text: str

# ----------------------------
# Root
# ----------------------------
@app.get("/")
def root():
    return {"status": "running"}

# ----------------------------
# S-CIAX ANALYZE ENGINE
# ----------------------------
@app.post("/analyze")
def analyze(input: InputModel):

    text = input.text
    text_lower = text.lower()

    # ----------------------------
    # Default values
    # ----------------------------
    stability_score = 0.9
    conflict_score = 0.1
    risk_level = "Low"
    reason = "Normal stable interaction detected"

    # ----------------------------
    # High risk keywords
    # ----------------------------
    high_risk_words = [
        "hack", "attack", "exploit", "bypass",
        "fraud", "steal", "destroy", "malware"
    ]

    # ----------------------------
    # Medium risk keywords
    # ----------------------------
    medium_risk_words = [
        "refund", "angry", "problem", "report",
        "complaint", "error", "broken"
    ]

    # ----------------------------
    # High risk detection
    # ----------------------------
    for word in high_risk_words:
        if word in text_lower:
            risk_level = "High"
            stability_score = 0.3
            conflict_score = 0.8
            reason = "Detected exploit or attack-related terminology"

    # ----------------------------
    # Medium risk detection
    # ----------------------------
    if risk_level != "High":
        for word in medium_risk_words:
            if word in text_lower:
                risk_level = "Medium"
                stability_score = 0.6
                conflict_score = 0.5
                reason = "Detected complaint or unstable interaction pattern"

    # ----------------------------
    # Length influence
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
    # FINAL RESPONSE (CLEAN JSON)
    # ----------------------------
    return {
        "input": text,
        "risk_level": risk_level,
        "stability_score": round(stability_score, 2),
        "conflict_score": round(conflict_score, 2),
        "reason": reason
    }
