from app.ingestion.vectorstore.chroma_store import ChromaStore
from app.ingestion.embeddings.embedding_service import EmbeddingService


query = "What is the company social media policy?"

query_embedding = EmbeddingService.generate_embeddings(
    [query]
)[0]

vector_store = ChromaStore()

results = vector_store.search(
    query_embedding=query_embedding,
    top_k=3
)

print(results)