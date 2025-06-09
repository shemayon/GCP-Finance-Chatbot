
from utils.embedding_utils import embed_text_chunks
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def search_similar_chunks(query, chunks, vectors, top_k=3):
    _, query_vecs = embed_text_chunks([query])
    query_vec = query_vecs[0].reshape(1, -1)

    similarities = cosine_similarity(query_vec, vectors)[0]
    top_indices = np.argsort(similarities)[-top_k:][::-1]

    return [chunks[i] for i in top_indices]