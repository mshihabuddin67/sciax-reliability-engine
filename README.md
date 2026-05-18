# ⚡ S-CIAX — Signal Classification & Risk Analysis Engine

> Lightweight · Explainable · Multilingual

S-CIAX is a real-time multilingual risk analysis API that detects threatening or harmful intent in text across Bangla, Romanized Bangla, Hindi, and English with structured, explainable output.

---

# 🌐 Live API

```bash
https://sciax-reliability-engine.onrender.com
```

---

# ✨ Features

- 🔍 Risk Classification — Low / Medium / High
- 🧠 Explainable Output — reason field explains every decision
- 🌏 Multilingual Support — Bangla, Romanized Bangla, Hindi, English
- ⚡ Lightweight Architecture — fast inference, low compute cost
- 🔗 API Ready — JSON input/output integration
- 🛡️ Context-Aware Detection — reduces false positives
- 📊 Dynamic Confidence Scoring — realistic explainable confidence estimation

---

#  Core Architecture

S-CIAX combines:

- multilingual normalization
- fuzzy semantic matching
- context-aware safe overrides
- explainable risk reasoning
- dynamic confidence scoring

to reduce false positives while preserving lightweight deployment architecture.

---

# 📡 API Usage

## Endpoint

```bash
POST /analyze
```

---

## Headers

```bash
x-api-key: sciax-demo-key-123
Content-Type: application/json
```

---

## Request Body

```json
{
  "text": "your input text here"
}
```

---

## Response

```json
{
  "input": "original text",
  "normalized_text": "processed text",
  "language_type": "latin / mixed_or_non_latin",
  "risk_level": "Low / Medium / High",
  "confidence_score": 0.92,
  "stability_score": 0.9,
  "conflict_score": 0.1,
  "reason": "explanation of decision"
}
```

---

# 🧪 Verified Results

| Input | Language | Risk | Confidence |
|---|---|---|---|
| "আমি তোমাকে শেষ করে দেব" | Bangla | 🔴 HIGH | 1.00 |
| "Ami tomake mere felbo" | Romanized Bangla | 🔴 HIGH | 1.00 |
| "tujhe mar dungga" | Romanized Hindi | 🔴 HIGH | 0.85 |
| "Hack the system" | English | 🔴 HIGH | 1.00 |
| "Hack my sleep schedule" | English | 🟢 LOW | 0.95 |
| "I need a productivity hack" | English | 🟢 LOW | 0.95 |
| "আজকের আবহাওয়া অনেক সুন্দর" | Bangla | 🟢 LOW | 0.6 |
| "I am angry" | English | 🟡 MEDIUM | 0.72 |

---

# 🔁 cURL Example

```bash
curl -X POST \
  'https://sciax-reliability-engine.onrender.com/analyze' \
  -H 'accept: application/json' \
  -H 'x-api-key: sciax-demo-key-123' \
  -H 'Content-Type: application/json' \
  -d '{"text": "Hack the system"}'
```

---

# 🐍 Python Example

```python
import requests

response = requests.post(
    "https://sciax-reliability-engine.onrender.com/analyze",
    headers={
        "x-api-key": "sciax-demo-key-123",
        "Content-Type": "application/json"
    },
    json={
        "text": "আমি তোমাকে শেষ করে দেব"
    }
)

print(response.json())
```

---

# 📊 Risk Level Guide

| Risk Level | Meaning | Example |
|---|---|---|
| 🟢 Low | Safe or normal interaction | "আজকের আবহাওয়া সুন্দর" |
| 🟡 Medium | Emotional instability or complaint-related interaction | "I am angry" |
| 🔴 High | Threatening, violent, or harmful intent | "আমি তোমাকে শেষ করে দেব" |

---

#  Supported Languages

| Language | Script | Example |
|---|---|---|
| English | Latin | "Hack the system" |
| Bangla | Bengali Script | "আমি তোমাকে শেষ করে দেব" |
| Romanized Bangla | Latin | "Ami tomake mere felbo" |
| Hindi / Romanized Hindi | Devanagari / Latin | "tujhe mar dungga" |

---

#  Tech Stack

- Framework — FastAPI
- Fuzzy Matching — RapidFuzz
- Deployment — Render
- Language — Python 3

---

#  Current Version

```bash
v8.0.0
```

---

# ⚠️ Current Limitations

- Deep semantic understanding is still limited
- Sarcasm and irony detection not yet supported
- Large-scale production traffic not validated
- Transformer-based semantic layer in development
- No adversarial robustness testing yet

---

# 🗺️ Roadmap

| Phase | Goal | Status |
|---|---|---|
| Phase 1 | Stable multilingual API | ✅ Done |
| Phase 2 | Semantic layer + contextual inference | 🔄 In Progress |
| Phase 3 | Dashboard + Authentication + SaaS API | 📅 Planned |
| Phase 4 | Benchmark evaluation + semantic embeddings | 📅 Planned |

---

#  Contributing

Feedback, testing, and contributions are welcome.

Open an issue or submit a pull request.

---

# 🌌 Vision

S-CIAX explores the idea that:

> Context matters more than isolated keywords.

The project focuses on lightweight explainable multilingual AI safety research for South Asian language environments.

---

# 📌 Project Status

Current stage:

```text
Explainable Multilingual Risk Analysis MVP
```

---

# ⚡ S-CIAX

Lightweight Explainable Multilingual Risk Analysis Engine.

---

# 👨‍💻 Author

**M Shehab**  
Independent builder exploring multilingual AI safety, contextual inference, and explainable risk analysis systems.
