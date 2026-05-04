from flask import Blueprint, request, jsonify
from core.engine import sciax_engine

analyze_route = Blueprint("analyze", __name__)

@analyze_route.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    prompt = data.get("prompt", "")

    result = sciax_engine(prompt)

    return jsonify(result)
