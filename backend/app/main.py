from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.perturb import perturb
from app.metrics import compute_metrics, compute_conflict
from app.risk import risk_analyzer
from app.response import build_response

app = FastAPI()
