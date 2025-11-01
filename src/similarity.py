from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


def calculate_similarity(resume_embedding, job_embedding):
    score = cosine_similarity([resume_embedding], [job_embedding])
    return score[0][0]


def calculate_all_similarities(resume_embeddings, job_embedding):
    scores = []
    for emb in resume_embeddings:
        scores.append(calculate_similarity(emb, job_embedding))
    return scores
