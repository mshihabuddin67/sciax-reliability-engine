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
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)
