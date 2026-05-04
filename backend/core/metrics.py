from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')

def compute_stability_score(variants):

    embeddings = model.encode(variants, convert_to_tensor=True)

    base = embeddings[0]

    scores = []

    for emb in embeddings:
        sim = util.cos_sim(base, emb).item()
        scores.append(sim)

    stability = sum(scores) / len(scores)

    return round(stability, 2)
