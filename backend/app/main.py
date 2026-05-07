from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Input schema
class InputModel(BaseModel):
    text: str

# Root route
@app.get("/")
def home():
    return {"status": "running"}

# Analyze route
@app.post("/analyze")
def analyze(input: InputModel):
    return {
        "received": input.text
    }
