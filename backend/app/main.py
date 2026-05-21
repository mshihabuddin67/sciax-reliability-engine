from fastapi import FastAPI

from backend.api.analyze import (
    analyze_route
)

from backend.app.config import (
    SYSTEM_MODE,
    SYSTEM_VERSION
)

app = FastAPI()

app.include_router(analyze_route)


@app.get("/")
def home():

    return {

        "status": "S-CIAX Running",

        "mode": SYSTEM_MODE,

        "version": SYSTEM_VERSION
    }
