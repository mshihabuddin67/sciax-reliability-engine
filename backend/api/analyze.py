@app.post("/analyze")
def analyze(input: InputModel):

    variants = perturb(input.text)[:3]  # limit

    outputs = [v + " response" for v in variants]

    metrics = compute_metrics(outputs)
    cs = compute_conflict(outputs)
    risk = risk_analyzer(metrics, cs)

    return build_response(input.text, metrics, cs, risk)
