def generate_variants(prompt):
    return [
        prompt,
        prompt + " please",
        prompt + " now",
        prompt.lower(),
        "Can you help me: " + prompt
    ]
