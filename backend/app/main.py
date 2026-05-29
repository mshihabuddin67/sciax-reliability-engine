from fastapi import FastAPI

from backend.api.analyze import (
    analyze_route
)

from backend.app.config import (
    SYSTEM_MODE,
    SYSTEM_VERSION
)

# ==================================================
# S-CIAX APPLICATION
# ==================================================

app = FastAPI(

    title="S-CIAX",

    description=(
        "Signal Classification & "
        "Risk Analysis Engine"
    ),

    version=SYSTEM_VERSION
)

# ==================================================
# ROUTES
# ==================================================

app.include_router(
    analyze_route
)

# ==================================================
# ROOT STATUS ENDPOINT
# ==================================================

@app.get("/")
def home():

    return {

        "status":
            "S-CIAX Running",

        "system_mode":
            SYSTEM_MODE,

        "system_version":
            SYSTEM_VERSION,

        "engine_type":
            "Hybrid Explainable Moderation Engine"
    }

# ==================================================
# HEALTH CHECK
# ==================================================

@app.get("/health")
def health_check():

    return {

        "status":
            "healthy",

        "service":
            "S-CIAX",

        "version":
            SYSTEM_VERSION
    }
