import math

from django.conf import settings

from .models import Chunk
from .ollama_client import embed


def cosine_similarity(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def get_relevant_chunks(query: str, top_k: int | None = None) -> list[Chunk]:
    """Embed the query and return the top_k most similar chunks (brute-force cosine).

    Fine for a personal knowledge base of a few hundred chunks; swap for pgvector's
    ANN index or a dedicated vector DB if this ever needs to scale further.
    """
    top_k = top_k or settings.RAG_TOP_K
    query_embedding = embed(query)

    scored = [
        (cosine_similarity(query_embedding, chunk.embedding), chunk)
        for chunk in Chunk.objects.select_related("document").all()
    ]
    scored.sort(key=lambda pair: pair[0], reverse=True)
    return [chunk for _, chunk in scored[:top_k]]
