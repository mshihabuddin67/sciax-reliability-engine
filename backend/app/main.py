from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# ----------------------------
# CORS FIX (IMPORTANT)
# ----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------
# Request Model
# ----------------------------
class InputModel(BaseModel):
    text: str

# ----------------------------
# Root check
# ----------------------------
@app.get("/")
def root():
    return {"status": "running"}

# ----------------------------
# S-CIAX Analyze Endpoint
# ----------------------------
@app.post("/analyze")
def analyze(input: InputModel):

    text = input.text

    # simple demo logic (safe for Render free tier)
    length = len(text)

    stability_score = max(0.1, min(1.0, 1 - (length / 200)))
    conflict_score = min(1.0, length / 150)

    if stability_score < 0.4:
        risk_level = "High"
    elif stability_score < 0.7:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    return {
        "input": text,
        "risk_level": risk_level,
        "stability_score": round(stability_score, 2),
        "conflict_score": round(conflict_score, 2)
    }
