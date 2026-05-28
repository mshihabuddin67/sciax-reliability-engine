def generate_variants(prompt):

    text = prompt.strip()

    variants = [

        # original
        text,

        # lowercase normalization
        text.lower(),

        # polite variation
        f"{text} please",

        # urgency variation
        f"{text} now",

        # helper/context variation
        f"can you help me: {text}",

        # conversational variation
        f"bro {text}",

        # intent-preserving variation
        f"please {text}",

        # spacing normalization
        text.replace("  ", " "),

        # punctuation variation
        f"{text}!",

        # multilingual-style perturbation
        text.replace("dibo", "debo"),

        text.replace("mar", "maar"),

        text.replace("hack", "haek")
    ]

    # -----------------------------------------
    # remove duplicates while preserving order
    # -----------------------------------------

    unique_variants = []

    for variant in variants:

        cleaned = variant.strip()

        if cleaned not in unique_variants:

            unique_variants.append(cleaned)

    return unique_variants
