from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.perturb import perturb
from app.metrics import compute_metrics, compute_conflict
from app.risk import risk_analyzer
from app.response import build_response

app = FastAPI()

#  CORS fix (frontend connect korar jonno)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#  Input schema
class InputModel(BaseModel):
    text: str

#  Main analysis endpoint
@app.post("/analyze")
def analyze(input: InputModel):

    # 1. Generate variants
    variants = perturb(input.text)

    # 2. Fake/demo outputs (replace later with real LLM if needed)
    outputs = [v + " response" for v in variants]

    # 3. Metrics calculation
    metrics = compute_metrics(outputs)
    cs = compute_conflict(outputs)

    # 4. Risk analysis
    risk = risk_analyzer(metrics, cs)

    # 5. Build final response
    return build_response(
        input.text,
        metrics,
        cs,
        risk
    )

# 🧪 Simple health check
@app.get("/")
def home():
    return {"message": "S-CIAX API is running"}
