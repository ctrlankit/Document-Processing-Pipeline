"""Chroma vector store integration."""

import chromadb
# Setup ephemeral client
client = chromadb.Client()

# Create collection
collection = client.create_collection(name="my_collection")

# Add documents
collection.add(
    documents=["This is document 1", "This is document 2"],
    metadatas=[{"source": "notion"}, {"source": "google"}],
    ids=["id1", "id2"]
)
