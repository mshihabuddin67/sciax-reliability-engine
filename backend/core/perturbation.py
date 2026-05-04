def generate_variants(prompt):
    return [
        prompt,
        prompt.lower(),
        prompt + " please",
        "I need: " + prompt,
        prompt.replace("I", "we"),
        prompt + " now"
    ]
