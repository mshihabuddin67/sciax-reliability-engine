from fastapi import FastAPI
import json

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
# REPORT CONFIG
# ==================================================

REPORT_PATH = "backend/reports/benchmark_results.json"


def load_report_data():

    try:

        with open(
            REPORT_PATH,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    except Exception:

        return []

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

# ==================================================
# BENCHMARK REPORTS
# ==================================================

@app.get("/reports")
def benchmark_reports():

    data = load_report_data()

    pass_count = sum(
        1 for item in data
        if item.get("status") == "PASS"
    )

    fail_count = sum(
        1 for item in data
        if item.get("status") != "PASS"
    )

    total = len(data)

    accuracy = (
        (pass_count / total) * 100
        if total > 0
        else 0
    )

    return {

        "total":
            total,

        "pass":
            pass_count,

        "fail":
            fail_count,

        "accuracy":
            round(accuracy, 2),

        "data":
            data
    }
