"""Document ingestion pipeline for EcoGen AI RAG assistant.

Loads local knowledge documents, chunks them, generates embeddings,
builds a FAISS vector store, and persists the index and chunk metadata.
"""

from __future__ import annotations

import pickle
from pathlib import Path
from typing import Any, Dict, Iterable, List, Sequence, Tuple

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


KNOWLEDGE_BASE_DIR = Path(__file__).resolve().parents[2] / "rag" / "documents"
VECTOR_STORE_DIR = Path(__file__).resolve().parents[2] / "rag" / "vectorstore" / "faiss_index"
SUPPORTED_EXTENSIONS = {"txt", "md"}
CHUNK_SIZE = 500
CHUNK_OVERLAP = 80
MODEL_NAME = "all-MiniLM-L6-v2"


def _ensure_vector_store_dir() -> None:
    VECTOR_STORE_DIR.mkdir(parents=True, exist_ok=True)


def _normalize_path(path: Path) -> str:
    return path.as_posix()


def _split_text_into_paragraphs(text: str) -> List[str]:
    paragraphs = [part.strip() for part in text.split("\n\n") if part.strip()]
    return paragraphs or [text.strip()]


def _build_chunk_text(text: str, start: int, end: int) -> str:
    return text[start:end].strip()


def load_documents() -> List[Dict[str, str]]:
    """Load supported documents with metadata for citations."""

    if not KNOWLEDGE_BASE_DIR.exists():
        raise FileNotFoundError(f"Knowledge base directory not found: {KNOWLEDGE_BASE_DIR}")

    documents: List[Dict[str, str]] = []

    for path in sorted(KNOWLEDGE_BASE_DIR.rglob("*")):
        if not path.is_file() or path.suffix.lower().lstrip(".") not in SUPPORTED_EXTENSIONS:
            continue

        try:
            content = path.read_text(encoding="utf-8", errors="ignore").strip()
        except OSError as error:
            raise IOError(f"Unable to read document {path}: {error}")

        if not content:
            continue

        documents.append(
            {
                "text": content,
                "source": _normalize_path(path.relative_to(KNOWLEDGE_BASE_DIR.parent.parent)),
                "title": path.stem,
            }
        )

    return documents


def chunk_documents(documents: Sequence[Dict[str, str]]) -> List[Dict[str, Any]]:
    """Split documents into overlapping text chunks with source metadata."""

    if not isinstance(documents, Sequence):
        raise TypeError("Documents must be provided as a sequence.")

    chunks: List[Dict[str, Any]] = []

    for document in documents:
        if not isinstance(document, dict):
            raise TypeError("Each document must be a dictionary with text and source metadata.")

        document_text = str(document.get("text", "")).strip()
        if not document_text:
            continue

        source = str(document.get("source", "unknown"))
        title = str(document.get("title", Path(source).stem))

        paragraphs = _split_text_into_paragraphs(document_text)
        current_buffer = ""

        for paragraph in paragraphs:
            if not paragraph:
                continue

            if current_buffer and len(current_buffer) + len(paragraph) > CHUNK_SIZE:
                chunks.append(
                    {
                        "text": current_buffer.strip(),
                        "source": source,
                        "title": title,
                    }
                )
                current_buffer = paragraph
            else:
                current_buffer = (
                    f"{current_buffer}\n\n{paragraph}".strip()
                    if current_buffer
                    else paragraph
                )

            if len(current_buffer) >= CHUNK_SIZE:
                start = 0
                end = min(CHUNK_SIZE, len(current_buffer))
                while start < len(current_buffer):
                    chunk_text = _build_chunk_text(current_buffer, start, end)
                    if chunk_text:
                        chunks.append(
                            {
                                "text": chunk_text,
                                "source": source,
                                "title": title,
                            }
                        )
                    if end >= len(current_buffer):
                        break
                    start = max(0, end - CHUNK_OVERLAP)
                    end = min(len(current_buffer), start + CHUNK_SIZE)

        if current_buffer:
            chunks.append(
                {
                    "text": current_buffer.strip(),
                    "source": source,
                    "title": title,
                }
            )

    return [chunk for chunk in chunks if chunk.get("text")]


def generate_embeddings(chunks: Sequence[Dict[str, Any]]) -> np.ndarray:
    """Generate embeddings for document chunks using a SentenceTransformer."""

    if not isinstance(chunks, Sequence):
        raise TypeError("Chunks must be provided as a sequence.")

    texts = [str(chunk.get("text", "")) for chunk in chunks if str(chunk.get("text", "")).strip()]
    if not texts:
        return np.empty((0, 384), dtype="float32")

    model = SentenceTransformer(MODEL_NAME)
    embeddings = model.encode(texts, show_progress_bar=False, convert_to_numpy=True)

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


def save_vector_store(index: faiss.IndexFlatL2, chunks: Sequence[Dict[str, Any]]) -> None:
    """Save the FAISS index and chunk metadata to the vector store directory."""

    _ensure_vector_store_dir()

    index_path = VECTOR_STORE_DIR / "index.faiss"
    chunks_path = VECTOR_STORE_DIR / "chunks.pkl"

    faiss.write_index(index, str(index_path))

    with chunks_path.open("wb") as handle:
        pickle.dump(list(chunks), handle)


def load_vector_store() -> Tuple[faiss.IndexFlatL2, List[Dict[str, Any]]]:
    """Load the FAISS index and chunk metadata from persistent storage."""

    index_path = VECTOR_STORE_DIR / "index.faiss"
    chunks_path = VECTOR_STORE_DIR / "chunks.pkl"

    if not index_path.exists() or not chunks_path.exists():
        raise FileNotFoundError("FAISS index or chunks file not found in vector store.")

    index = faiss.read_index(str(index_path))

    with chunks_path.open("rb") as handle:
        chunks = pickle.load(handle)

    if not isinstance(chunks, list):
        raise ValueError("Loaded chunks data is not a list.")

    normalized_chunks: List[Dict[str, Any]] = []
    for chunk in chunks:
        if isinstance(chunk, dict):
            normalized_chunks.append(
                {
                    "text": str(chunk.get("text", "")),
                    "source": str(chunk.get("source", "unknown")),
                    "title": str(chunk.get("title", Path(chunk.get("source", "unknown")).stem)),
                }
            )
        else:
            normalized_chunks.append(
                {
                    "text": str(chunk),
                    "source": "unknown",
                    "title": "unknown",
                }
            )

    return index, normalized_chunks


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
