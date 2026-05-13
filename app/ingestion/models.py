"""Shared ingestion data models."""

from dataclasses import dataclass


@dataclass
class ChunkDocument:

    chunk_id: str

    text: str

    source_file: str

    chunk_index: int

    document_hash: str

    embedding_model: str