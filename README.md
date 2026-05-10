# S-CIAX

Explainable Signal Classification & Risk Analysis Engine

---

## Overview

S-CIAX is a lightweight explainable analysis engine designed to classify text inputs into structured behavioral signals.

The system analyzes user input and produces:

- Risk Level
- Stability Score
- Conflict Score
- Explainable Reason Output

---

## Features

- Explainable risk analysis
- Structured JSON responses
- FastAPI backend
- Mobile-friendly dashboard
- Live API integration
- Research-oriented interface

---

## Example Response

```json
{
  "input": "hack the system",
  "risk_level": "High",
  "stability_score": 0.3,
  "conflict_score": 0.8,
  "reason": "Detected exploit or attack-related terminology"
}
```

---

## Tech Stack

### Backend
- Python
- FastAPI

### Frontend
- HTML
- CSS
- JavaScript

---

## Project Structure

```bash
sciax-project/

├── backend/
│   └── app/
│       └── main.py
│
├── frontend/
│   └── index.html
│
├── README.md
```

---

## API Endpoint

### POST `/analyze`

Example Request:

```json
{
  "text": "hack the system"
}
```

---

## Current System Capabilities

- Rule-based signal analysis
- Risk classification
- Explainability layer
- Structured scoring system

---

## Future Roadmap

- Semantic analysis
- Adaptive scoring
- API key management
- Usage analytics
- SaaS dashboard
- Research visualization tools

---

## Status

Active Prototype / Research Demo

---

## Author

M Shehab
