"""Chroma vector store integration."""

import chromadb


class ChromaStore:

    def __init__(self):

        self.client = chromadb.PersistentClient(path="data/vectorstore")

        self.collection = self.client.get_or_create_collection(name="documents")

    def add_documents(self, chunk_documents, embeddings):

        ids = []
        documents = []
        metadatas = []

        for chunk_doc in chunk_documents:

            ids.append(chunk_doc.chunk_id)

            documents.append(chunk_doc.text)

            metadatas.append(
                {
                    "source_file": chunk_doc.source_file,
                    "chunk_index": chunk_doc.chunk_index,
                    "document_hash": chunk_doc.document_hash,
                    "embedding_model": chunk_doc.embedding_model,
                }
            )

        self.collection.upsert(
            ids=ids,
            documents=documents,
            embeddings=embeddings.tolist(),
            metadatas=metadatas,
        )

        print(f"Stored {len(ids)} chunks in ChromaDB")

    def search(self, query_embedding, top_k=3):

        results = self.collection.query(
            query_embeddings=[query_embedding.tolist()], n_results=top_k
        )

        return results
