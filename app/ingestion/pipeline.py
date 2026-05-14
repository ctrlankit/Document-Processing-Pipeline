"""Pipeline orchestration for document ingestion."""

import os

from app.ingestion.metadata.hash_manager import HashManager

from app.ingestion.loaders.pdf_loader import PDFLoader
from app.ingestion.loaders.docx_loader import DOCXLoader
from app.ingestion.loaders.excel_loader import ExcelLoader

from app.ingestion.chunking.text_chunker import TextChunker

from app.ingestion.embeddings.embedding_service import EmbeddingService
from app.ingestion.vectorstore.chroma_store import ChromaStore

from app.ingestion.models import ChunkDocument
import uuid


class Pipeline:

    def process_file(self, file_path):

        # STEP 1 — Check incremental ingestion
        is_changed = HashManager.is_file_changed(file_path)

        if not is_changed:

            print(f"Skipping unchanged file: {file_path}")

            return

        print(f"Processing changed file: {file_path}")

        # STEP 2 — Detect file type
        extension = os.path.splitext(file_path)[1].lower()

        text = ""

        # STEP 3 — Extract text
        if extension == ".pdf":

            text = PDFLoader.load(file_path)

        elif extension == ".docx":

            text = DOCXLoader.load(file_path)

        elif extension == ".xlsx":

            text = ExcelLoader.extract_text(file_path)

        else:

            print(f"Unsupported file type: {extension}")

            return

        # Safety check
        if not text.strip():

            print("No text extracted from document")

            return

        # STEP 4 — Chunking
        chunks = TextChunker.chunk_text(text)

        print(f"Total chunks created: {len(chunks)}")

        # STEP 5 — Generate document hash
        document_hash = HashManager.Generate_hash(file_path)

        # STEP 6 — Create structured chunk documents
        chunk_documents = []

        for index, chunk in enumerate(chunks):

            chunk_doc = ChunkDocument(

                chunk_id=f"{document_hash}_{index}",

                text=chunk,

                source_file=file_path,

                chunk_index=index,

                document_hash=document_hash,

                embedding_model="all-MiniLM-L6-v2"
            )

            chunk_documents.append(chunk_doc)

        # STEP 7 — Generate embeddings
        chunk_texts = [
            chunk.text
            for chunk in chunk_documents
        ]

        embeddings = EmbeddingService.generate_embeddings(
            chunk_texts
        )

        print(f"Generated {len(embeddings)} embeddings")

        # STEP 8 — Store embeddings
        store = ChromaStore()

        store.add_documents(
            chunk_documents,
            embeddings
        )

        print(f"Completed processing for file: {file_path}")


        # # STEP 8 — Print sample output
        # for i, chunk_doc in enumerate(chunk_documents):

        #     print("\n====================")
        #     print(f"Chunk {i + 1}")
        #     print("====================")

        #     print(f"Chunk ID: {chunk_doc.chunk_id}")

        #     print(f"Source File: {chunk_doc.source_file}")

        #     print(f"Chunk Index: {chunk_doc.chunk_index}")

        #     print(f"Embedding Model: {chunk_doc.embedding_model}")

        #     print(f"Text:\n{chunk_doc.text[:300]}")

        #     print(f"Embedding Dimension: {len(embeddings[i])}")

        #     print("====================\n")