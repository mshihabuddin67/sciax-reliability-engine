from fastapi import APIRouter
from pydantic import BaseModel

from backend.core.normalization import (
    normalize_text
)

from backend.core.engine import (
    sciax_engine
)

from backend.core.behavioral_signals import (
    detect_behavioral_signals
)

from backend.core.intent_engine import (
    classify_intent
)

from backend.core.language_profiles import (
    detect_language_profile
)

from backend.core.explainability import (
    generate_explanations
)

from backend.app.response import (
    build_response
)

analyze_route = APIRouter()


class InputModel(BaseModel):

    text: str


@analyze_route.post("/analyze")
def analyze(input: InputModel):

    text = input.text

    normalized = normalize_text(text)

    engine_output = sciax_engine(
        normalized
    )

    behavioral = detect_behavioral_signals(
        normalized
    )

    intent = classify_intent(
        normalized
    )

    language = detect_language_profile(
        text
    )

    explainability = generate_explanations(
        normalized
    )

    response = build_response(

        input_text=text,

        engine_output=engine_output,

        behavioral_signals=behavioral,

        intent_classification=intent,

        language_profile=language,

        explainability=explainability
    )

    return response
