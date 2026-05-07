@app.post("/analyze")
def analyze(input: InputModel):

    # Generate variants
    variants = perturb(input.text)

    # Demo outputs
    outputs = [v + " response" for v in variants]

    # Metrics
    metrics = compute_metrics(outputs)

    # Conflict score
    cs = compute_conflict(outputs)

    # Risk analysis
    risk = risk_analyzer(metrics, cs)

    # Final response
    return build_response(
        input.text,
        metrics,
        cs,
        risk
    )
