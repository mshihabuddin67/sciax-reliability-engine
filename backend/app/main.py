from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rapidfuzz import fuzz
import re

from backend.app.config import (
    API_KEYS,
    DEFAULT_STABILITY,
    DEFAULT_CONFLICT,
    DEFAULT_RISK,
    MULTI_LANG_RISK
)

app = FastAPI()

# --------------------------------------------------
# CORS
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------------------------
# INPUT MODEL
# --------------------------------------------------

class InputModel(BaseModel):
    text: str

# --------------------------------------------------
# API KEY VERIFY
# --------------------------------------------------

def verify_key(api_key: str):

    if not api_key:

        raise HTTPException(
            status_code=401,
            detail="API key missing"
        )

    if api_key not in API_KEYS:

        raise HTTPException(
            status_code=403,
            detail="Invalid API key"
        )

# --------------------------------------------------
# LANGUAGE SAFE DETECTION
# --------------------------------------------------

def detect_language_safe(text: str) -> str:

    has_bangla = bool(
        re.search(r'[\u0980-\u09FF]', text)
    )

    has_hindi = bool(
        re.search(r'[\u0900-\u097F]', text)
    )

    if has_bangla or has_hindi:
        return "mixed_or_non_latin"

    return "latin"

# --------------------------------------------------
# NORMALIZATION
# --------------------------------------------------

def normalize_text(text: str) -> str:

    text = text.lower().strip()

    # remove extra spaces
    text = re.sub(r'\s+', ' ', text)

# --------------------------------------------------
# REPLACEMENT 
# --------------------------------------------------
    
    replacements = {

    # hack variations
    "haek": "hack",
    "hek": "hack",
    "hax": "hack",
    "hyack": "hack",

    # destroy variations
    "dhongsho": "destroy",
    "borbad": "destroy",

    # steal variations
    "churi": "steal",
    "data churi": "steal data",

    # attack
    "hamla": "attack",

    # system intent
    "system bhangbo": "destroy system",
    "system bhang": "destroy system",

    # bypass
    "bypass korbo": "bypass",
    "bypass kori": "bypass",

    # violence transliteration
    "mere felbo": "kill you",
    "khun korbo": "murder",
    "jaan mere dibo": "kill you",

    # bangla indirect threats
    "শেষ করে দিব": "kill you",
    "শেষ করে দেব": "kill you",

    "shesh kore dibo": "kill you",
    "shesh kore debo": "kill you",

    "উড়িয়ে দিব": "destroy",

    "ধ্বংস করে দিব": "destroy system",

    "তোকে দেখে নিব": "threat intent",
    "toke dekhe nibo": "threat intent"
    }

    for wrong, correct in replacements.items():

        if wrong in text:
            text = text.replace(wrong, correct)

    return text

# --------------------------------------------------
# SAFE CONTEXTS
# --------------------------------------------------

SAFE_CONTEXTS = [

    "sleep schedule",
    "productivity hack",
    "study hack",
    "life hack",

    "game level",
    "gaming strategy",

    "kill time",
    "destroy boredom",

    "football attack",
    "attack strategy"
]

# --------------------------------------------------
# HIGH RISK PATTERNS
# --------------------------------------------------

HIGH_RISK_PATTERNS = [

    # cyber
    "hack the system",
    "bypass security",
    "steal data",
    "destroy system",
    "attack server",
    "exploit vulnerability",

    # violence english
    "kill you",
    "kill everyone",
    "murder you",
    "burn the house",
    "i will kill you",
    "destroy you",

    # indirect threats
    "threat intent",

    # banglish
    "mere felbo",
    "khun korbo",
    "jaan mere dibo",

    "shesh kore dibo",
    "shesh kore debo",

    "toke dekhe nibo",

    # bangla
    "মেরে ফেলবো",
    "খুন করবো",
    "জান মেরে দিবো",

    "শেষ করে দিব",
    "শেষ করে দেব",

    "উড়িয়ে দিব",
    "ধ্বংস করে দিব",

    "তোকে দেখে নিব",

    # hindi
    "jaan se mar dunga",
    "maar dunga"
]

# --------------------------------------------------
# MEDIUM RISK WORDS
# --------------------------------------------------

MEDIUM_RISK_WORDS = [

    "angry",
    "problem",
    "broken",
    "refund",
    "complaint",
    "issue",
    "error",
    "bad service",

    # banglish
    "rag",
    "somossa",
    "kharap",

    # hindi
    "gussa",
    "samasya"
]

# --------------------------------------------------
# ROOT
# --------------------------------------------------

@app.get("/")
def root():

    return {

        "status": "S-CIAX Running",
        "version": "7.0.0"
    }

# --------------------------------------------------
# ANALYZE
# --------------------------------------------------

@app.post("/analyze")
def analyze(
    input: InputModel,
    x_api_key: str = Header(None)
):

    verify_key(x_api_key)

    original_text = input.text

    language_type = detect_language_safe(
        original_text
    )

    text = normalize_text(original_text)

    # --------------------------------------------------
    # DEFAULT
    # --------------------------------------------------

    risk_level = DEFAULT_RISK

    stability_score = DEFAULT_STABILITY
    conflict_score = DEFAULT_CONFLICT

    confidence_score = 0.55

    reason = "Normal stable interaction detected"

    safe_detected = False

    # --------------------------------------------------
    # SAFE CONTEXT CHECK
    # --------------------------------------------------

    for safe in SAFE_CONTEXTS:

        if safe in text:

            safe_detected = True

            risk_level = "Low"

            stability_score = 0.9
            conflict_score = 0.1

            confidence_score = 0.92

            reason = (
                f"Safe context detected ({safe})"
            )

            break

    # --------------------------------------------------
    # HIGH RISK CHECK
    # --------------------------------------------------

    if not safe_detected:

        for pattern in HIGH_RISK_PATTERNS:

            similarity = fuzz.partial_ratio(
                text,
                pattern
            )

            if similarity >= 80:

                risk_level = "High"

                stability_score = 0.3
                conflict_score = 0.8

                confidence_score = round(
                    similarity / 100,
                    2
                )

                # violence reasoning
                if (

                    "kill" in pattern or
                    "murder" in pattern or
                    "মেরে ফেলবো" in pattern or
                    "খুন" in pattern or
                    "maar dunga" in pattern

                ):

                    reason = (
                        "High risk violent intent detected"
                    )

                else:

                    reason = (
                        f"High risk intent detected "
                        f"({pattern})"
                    )

                break

    # --------------------------------------------------
    # MULTILINGUAL RISK
    # --------------------------------------------------

    if risk_level != "High" and not safe_detected:

        for category, words in MULTI_LANG_RISK.items():

            for word in words:

                if word.lower() in text:

                    risk_level = "High"

                    stability_score = 0.3
                    conflict_score = 0.8

                    confidence_score = 0.85

                    if category == "violence":

                        reason = (
                            "Multilingual violent "
                            "intent detected"
                        )

                    else:

                        reason = (
                            f"Multilingual risky signal "
                            f"detected ({category})"
                        )

                    break

    # --------------------------------------------------
    # MEDIUM RISK
    # --------------------------------------------------

    if risk_level != "High":

        for word in MEDIUM_RISK_WORDS:

            if word in text:

                risk_level = "Medium"

                stability_score = 0.6
                conflict_score = 0.5

                confidence_score = 0.72

                reason = (
                    "Detected unstable or "
                    "complaint-related interaction"
                )

                break

# --------------------------------------------------
# DYNAMIC CONFIDENCE SYSTEM
# --------------------------------------------------

signal_count = 0

# count multilingual risk signals
for category, words in MULTI_LANG_RISK.items():

    for word in words:

        if word.lower() in text:
            signal_count += 1

# boost confidence from signals
confidence_score += signal_count * 0.03

# multilingual confidence boost
if language_type == "mixed_or_non_latin":

    confidence_score += 0.05

# long input uncertainty
if len(text.split()) > 20:

    confidence_score -= 0.05

# safe context stabilization
if safe_detected:

    confidence_score = max(
        confidence_score,
        0.90
    )

# medium ambiguity balancing
if risk_level == "Medium":

    confidence_score = min(
        confidence_score,
        0.80
    )

# high risk confidence floor
if risk_level == "High":

    confidence_score = max(
        confidence_score,
        0.85
    )

# final clamp
confidence_score = max(
    0.0,
    min(1.0, confidence_score)
)
    # --------------------------------------------------
    # LONG INPUT EFFECT
    # --------------------------------------------------

    if len(text) > 120:

        stability_score -= 0.1
        conflict_score += 0.1

    # --------------------------------------------------
    # CLAMP
    # --------------------------------------------------

    stability_score = max(
        0.1,
        min(1.0, stability_score)
    )

    conflict_score = max(
        0.0,
        min(1.0, conflict_score)
    )

    confidence_score = max(
        0.0,
        min(1.0, confidence_score)
    )

    # --------------------------------------------------
    # RESPONSE
    # --------------------------------------------------

    return {

        "input": original_text,

        "normalized_text": text,

        "language_type": language_type,

        "risk_level": risk_level,

        "confidence_score": round(
            confidence_score,
            2
        ),

        "stability_score": round(
            stability_score,
            2
        ),

        "conflict_score": round(
            conflict_score,
            2
        ),

        "reason": reason
        }
