from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from sentence_transformers import SentenceTransformer, util

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
# SIMPLE API KEY (demo)
# ----------------------------
VALID_API_KEYS = {
    "sciax-demo-key-123": "user_1"
}

# ----------------------------
# MODEL (Semantic Layer)
# ----------------------------
model = SentenceTransformer("all-MiniLM-L6-v2")

RISK_SIGNALS = [
    "hack the system",
    "exploit security",
    "break into system",
    "steal data",
    "malware attack",
    "bypass authentication"
]

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
    if api_key not in VALID_API_KEYS:
        raise HTTPException(status_code=403, detail="Invalid API key")

# ----------------------------
# ROOT
# ----------------------------
@app.get("/")
def root():
    return {"status": "S-CIAX Semantic Engine Active"}

# ----------------------------
# ANALYZE ENDPOINT
# ----------------------------
@app.post("/analyze")
def analyze(input: InputModel, x_api_key: str = Header(None)):

    verify_key(x_api_key)

    text = input.text.lower()

    # ----------------------------
    # BASE RULE ENGINE
    # ----------------------------
    risk_level = "Low"
    stability_score = 0.9
    conflict_score = 0.1
    reason = "Normal stable interaction detected"

    high_risk_words = ["hack", "attack", "exploit", "steal", "malware"]
    medium_risk_words = ["refund", "problem", "complaint", "error"]

    # HIGH RISK RULES
    for w in high_risk_words:
        if w in text:
            risk_level = "High"
            stability_score = 0.3
            conflict_score = 0.8
            reason = "Rule-based high risk detected"

    # MEDIUM RISK RULES
    if risk_level != "High":
        for w in medium_risk_words:
            if w in text:
                risk_level = "Medium"
                stability_score = 0.6
                conflict_score = 0.5
                reason = "Moderate instability detected"

    # ----------------------------
    # SEMANTIC INTELLIGENCE LAYER
    # ----------------------------
    input_emb = model.encode(text, convert_to_tensor=True)
    signal_emb = model.encode(RISK_SIGNALS, convert_to_tensor=True)

    similarity = util.cos_sim(input_emb, signal_emb)
    max_sim = float(similarity.max())

    # Semantic boosting
    if max_sim > 0.75:
        risk_level = "High"
        stability_score = min(stability_score, 0.35)
        conflict_score = max(conflict_score, 0.75)
        reason = "Semantic high-risk pattern detected"

    elif max_sim > 0.5 and risk_level != "High":
        risk_level = "Medium"
        stability_score = 0.6
        conflict_score = 0.5
        reason = "Semantic similarity detected"

    # ----------------------------
    # RESPONSE
    # ----------------------------
    return {
        "input": input.text,
        "risk_level": risk_level,
        "stability_score": round(stability_score, 2),
        "conflict_score": round(conflict_score, 2),
        "semantic_score": round(max_sim, 2),
        "reason": reason,
        "api_status": "authorized"
    }
