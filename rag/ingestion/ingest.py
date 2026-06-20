"""Document ingestion pipeline for EcoGen AI RAG assistant.

Loads local knowledge documents, chunks them, generates embeddings,
builds a FAISS vector store, and persists the index and chunks.
"""

from __future__ import annotations

import pickle
from pathlib import Path
from typing import Any, List, Tuple

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


KNOWLEDGE_BASE_DIR = Path(__file__).resolve().parents[2] / "rag" / "documents"
VECTOR_STORE_DIR = Path(__file__).resolve().parents[2] / "rag" / "vectorstore" / "faiss_index"
SUPPORTED_EXTENSIONS = {"txt", "md"}
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
MODEL_NAME = "all-MiniLM-L6-v2"


def _ensure_vector_store_dir() -> None:
    VECTOR_STORE_DIR.mkdir(parents=True, exist_ok=True)


def load_documents() -> List[str]:
    """Load all supported documents recursively from the knowledge base."""

    if not KNOWLEDGE_BASE_DIR.exists():
        raise FileNotFoundError(f"Knowledge base directory not found: {KNOWLEDGE_BASE_DIR}")

    documents: List[str] = []

    for path in sorted(KNOWLEDGE_BASE_DIR.rglob("*")):
        if path.is_file() and path.suffix.lower().lstrip(".") in SUPPORTED_EXTENSIONS:
            try:
                content = path.read_text(encoding="utf-8", errors="ignore").strip()
            except OSError as error:
                raise IOError(f"Unable to read document {path}: {error}")

            if content:
                documents.append(content)

    return documents


def chunk_documents(documents: List[str]) -> List[str]:
    """Split documents into overlapping text chunks."""

    if not isinstance(documents, list):
        raise TypeError("Documents must be provided as a list of strings.")

    chunks: List[str] = []

    for document in documents:
        if not isinstance(document, str):
            raise TypeError("Each document must be a string.")

        position = 0
        text_length = len(document)

        while position < text_length:
            end = position + CHUNK_SIZE
            chunk = document[position:end]
            chunks.append(chunk.strip())

            if end >= text_length:
                break

            position = max(0, end - CHUNK_OVERLAP)

    return [chunk for chunk in chunks if chunk]


def generate_embeddings(chunks: List[str]) -> np.ndarray:
    """Generate embeddings for document chunks using a SentenceTransformer."""

    if not isinstance(chunks, list):
        raise TypeError("Chunks must be provided as a list of strings.")

    if not chunks:
        return np.empty((0, 384), dtype="float32")

    model = SentenceTransformer(MODEL_NAME)
    embeddings = model.encode(chunks, show_progress_bar=False, convert_to_numpy=True)

    if embeddings.ndim != 2:
        raise ValueError("Unexpected embedding shape from SentenceTransformer.")

    return embeddings.astype("float32")


def build_vector_store(embeddings: np.ndarray) -> faiss.IndexFlatL2:
    """Create a FAISS IndexFlatL2 and add embeddings."""

    if embeddings.ndim != 2:
        raise ValueError("Embeddings must be a 2D NumPy array.")

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    return index


def save_vector_store(index: faiss.IndexFlatL2, chunks: List[str]) -> None:
    """Save the FAISS index and chunk list to the vector store directory."""

    _ensure_vector_store_dir()

    index_path = VECTOR_STORE_DIR / "index.faiss"
    chunks_path = VECTOR_STORE_DIR / "chunks.pkl"

    faiss.write_index(index, str(index_path))

    with chunks_path.open("wb") as handle:
        pickle.dump(chunks, handle)


def load_vector_store() -> Tuple[faiss.IndexFlatL2, List[str]]:
    """Load the FAISS index and chunk list from persistent storage."""

    index_path = VECTOR_STORE_DIR / "index.faiss"
    chunks_path = VECTOR_STORE_DIR / "chunks.pkl"

    if not index_path.exists() or not chunks_path.exists():
        raise FileNotFoundError("FAISS index or chunks file not found in vector store.")

    index = faiss.read_index(str(index_path))

    with chunks_path.open("rb") as handle:
        chunks = pickle.load(handle)

    if not isinstance(chunks, list):
        raise ValueError("Loaded chunks data is not a list.")

    return index, chunks


if __name__ == "__main__":
    documents = load_documents()
    chunks = chunk_documents(documents)
    embeddings = generate_embeddings(chunks)
    index = build_vector_store(embeddings)
    save_vector_store(index, chunks)

    print(f"Documents Loaded: {len(documents)}")
    print(f"Chunks Created: {len(chunks)}")
    print(f"Embeddings Generated: {embeddings.shape[0]}")
    print("FAISS Index Created")
    print("Vector Store Saved")
    print("\n" + "=" * 50)
