# Document Processing Pipeline

A Python-based document ingestion pipeline that extracts text from files, splits the content into chunks, generates embeddings with `sentence-transformers`, and stores the results in ChromaDB for semantic retrieval.

The project is structured for retrieval-augmented workflows: ingest documents once, skip unchanged files using hashes, and run similarity search over stored chunks.

## Features

- Incremental ingestion using file hashes stored in `data/processed/file_hashes.json`
- Text extraction for `PDF`, `DOCX`, and `XLSX` files
- Chunking with LangChain's `RecursiveCharacterTextSplitter`
- Embedding generation with `all-MiniLM-L6-v2`
- Persistent vector storage with ChromaDB
- Basic FastAPI app scaffold for exposing the pipeline as an API

## Project Structure

```text
Document Processing Pipeline/
|-- app/
|   |-- api/
|   |   `-- V1/routes.py
|   |-- config/
|   |   `-- settings.py
|   `-- ingestion/
|       |-- chunking/
|       |-- embeddings/
|       |-- loaders/
|       |-- metadata/
|       |-- vectorstore/
|       |-- models.py
|       `-- pipeline.py
|-- data/
|   |-- processed/
|   |   `-- file_hashes.json
|   `-- raw/
|-- main.py
|-- requirements.txt
|-- test_retrieval.py
`-- test_scripts.py
```

## How It Works

1. A file is passed to `Pipeline.process_file(...)`.
2. The pipeline computes a hash and skips the file if it has not changed.
3. Text is extracted based on file extension.
4. The extracted text is split into chunks.
5. Each chunk is wrapped with metadata such as source file, chunk index, and document hash.
6. Embeddings are generated using `all-MiniLM-L6-v2`.
7. Chunks and embeddings are stored in a persistent ChromaDB collection at `data/vectorstore`.

## Current Supported File Types

The pipeline in [app/ingestion/pipeline.py](app/ingestion/pipeline.py) currently processes:

- `.pdf`
- `.docx`
- `.xlsx`

Additional loader files exist for OCR and HTML, but they are not currently wired into the main ingestion flow.

## Requirements

- Python 3.10+
- `pip`

Depending on your environment, OCR support may also require a local Tesseract installation because `pytesseract` is included in the dependencies.

## Installation

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

### Ingest a document

The repository already includes a simple ingestion script in [test_scripts.py](test_scripts.py).

```python
from app.ingestion.pipeline import Pipeline

pipeline = Pipeline()
pipeline.process_file("data/raw/ComapnyPolicy.pptx.pdf")
```

Run it with:

```bash
python test_scripts.py
```

### Run a semantic search

The repository includes a retrieval example in [test_retrieval.py](test_retrieval.py).

```bash
python test_retrieval.py
```

This script:

- converts a query into an embedding
- searches the ChromaDB collection
- prints the top matching chunks

### Start the API server

The FastAPI app currently exposes a simple health-style root endpoint from [main.py](main.py).

```bash
uvicorn main:app --reload
```

Then open:

```text
http://127.0.0.1:8000/
```

Expected response:

```json
{"status":"200","message":"server is running"}
```

## Core Components

- [app/ingestion/pipeline.py](app/ingestion/pipeline.py): orchestrates the ingestion workflow
- [app/ingestion/loaders/pdf_loader.py](app/ingestion/loaders/pdf_loader.py): extracts text from PDFs
- [app/ingestion/loaders/docx_loader.py](app/ingestion/loaders/docx_loader.py): extracts text from Word documents
- [app/ingestion/loaders/excel_loader.py](app/ingestion/loaders/excel_loader.py): converts Excel sheets into text
- [app/ingestion/chunking/text_chunker.py](app/ingestion/chunking/text_chunker.py): splits text into overlapping chunks
- [app/ingestion/embeddings/embedding_service.py](app/ingestion/embeddings/embedding_service.py): loads the embedding model and encodes text
- [app/ingestion/vectorstore/chroma_store.py](app/ingestion/vectorstore/chroma_store.py): persists embeddings and performs similarity search
- [app/ingestion/metadata/hash_manager.py](app/ingestion/metadata/hash_manager.py): tracks changes using file hashes

## Data Storage

- Raw input files live in `data/raw/`
- Processed file hashes are stored in `data/processed/file_hashes.json`
- ChromaDB persistent storage is created in `data/vectorstore/`

## Notes

- Embeddings are currently generated locally with `sentence-transformers`; no external embedding API is required.
- File identity for incremental ingestion is tracked by base filename in the hash file, not full path.
- The `app/api/V1/routes.py` and `app/config/settings.py` modules are currently placeholders.

## Next Improvements

- Connect the pipeline to FastAPI upload and search endpoints
- Add support for OCR/image-based PDFs through the existing OCR loader
- Add HTML ingestion support
- Expand tests for ingestion, chunking, and retrieval behavior
- Move hardcoded paths and model configuration into `settings.py`

## License

Add your preferred license here.
