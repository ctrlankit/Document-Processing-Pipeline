"""Embedding service."""

from sentence_transformers import SentenceTransformer


class EmbeddingService:

    model = SentenceTransformer(
        "all-MiniLM-L6-v2"
    )

    @staticmethod
    def generate_embeddings(texts):

        embeddings = EmbeddingService.model.encode(texts)

        return embeddings