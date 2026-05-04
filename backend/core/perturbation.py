def generate_variants(prompt):
    return [
        prompt,
        prompt + " please",
        "I need: " + prompt,
        prompt.replace("I", "we")
    ]
