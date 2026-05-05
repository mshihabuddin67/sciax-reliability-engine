
# S-CIAX Demo

AI Output Stability & Failure Detection System

##  Live API
https://sciax-reliability-engine.onrender.com

##  What it does
Detects when AI outputs become unstable under small input variations.

## 🖥️ Demo

1. Open frontend/index.html
2. Enter a prompt (e.g. "I want a refund")
3. Click Analyze
4. View:
   - Stability score
   - Risk level
   - Variants
   - Outputs

 API Usage

POST /analyze

{
  "text": "I want a refund"
}
