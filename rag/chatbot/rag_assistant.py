"""Retrieval-Augmented Generation (RAG) assistant interface.

Implements a semantic sustainability knowledge assistant using FAISS and
sentence-transformers embeddings.
"""

from __future__ import annotations

import pickle
from pathlib import Path
from typing import Any, Dict, List

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

ContextChunk = Dict[str, str]
AnswerPackage = Dict[str, Any]

VECTOR_STORE_DIR = Path(__file__).resolve().parents[2] / "rag" / "vectorstore" / "faiss_index"
INDEX_PATH = VECTOR_STORE_DIR / "index.faiss"
CHUNKS_PATH = VECTOR_STORE_DIR / "chunks.pkl"
MODEL_NAME = "all-MiniLM-L6-v2"


def _embed_question(question: str) -> np.ndarray:
    """Embed a question using the sentence transformer model."""

    model = SentenceTransformer(MODEL_NAME)
    embedding = model.encode([question], show_progress_bar=False, convert_to_numpy=True)

    if embedding.ndim != 2:
        raise ValueError("Unexpected embedding shape from sentence-transformer model.")

    return embedding.astype("float32")


def load_vector_store() -> tuple[faiss.Index, List[str]]:
    """Load the FAISS index and chunk data from disk."""

    if not INDEX_PATH.exists() or not CHUNKS_PATH.exists():
        raise FileNotFoundError(
            f"Vector store not found. Expected files: {INDEX_PATH}, {CHUNKS_PATH}"
        )

    index = faiss.read_index(str(INDEX_PATH))

    with CHUNKS_PATH.open("rb") as handle:
        chunks = pickle.load(handle)

    if not isinstance(chunks, list):
        raise ValueError("Loaded chunks file does not contain a list of strings.")

    return index, chunks


def retrieve_context(question: str, top_k: int = 3) -> List[ContextChunk]:
    """Retrieve the top matching document chunks for a question using FAISS."""

    if not isinstance(question, str):
        raise TypeError("Question must be a string.")

    if not question.strip():
        return []

    if not isinstance(top_k, int) or top_k <= 0:
        raise ValueError("top_k must be a positive integer.")

    index, chunks = load_vector_store()
    question_embedding = _embed_question(question)
    distances, indices = index.search(question_embedding, top_k)

    context_chunks: List[ContextChunk] = []

    for idx in indices[0]:
        if idx < 0 or idx >= len(chunks):
            continue

        chunk_text = chunks[idx]
        if not isinstance(chunk_text, str):
            continue

        context_chunks.append({"text": chunk_text, "source": f"chunk_{idx}"})

    return context_chunks


def generate_answer(question: str, context: List[ContextChunk]) -> str:
    """Generate a grounded answer using the question and retrieved content."""

    if not isinstance(question, str):
        raise TypeError("Question must be a string.")

    if not question.strip():
        raise ValueError("Question cannot be empty.")

    if not context:
        return "I could not find sufficient sustainability information in the knowledge base."

    referenced_texts = [chunk["text"] for chunk in context[:3] if chunk.get("text")]
    combined_context = "\n\n".join(referenced_texts)

    return (
        "Based on the retrieved sustainability knowledge, here is an answer to your question:\n\n"
        f"{combined_context}\n\n"
        "In summary, the retrieved context provides grounded sustainability insights related to your query."
    )


def ask_question(question: str) -> AnswerPackage:
    """Ask a sustainability question and return the retrieved context and answer."""

    if not isinstance(question, str):
        raise TypeError("Question must be a string.")

    retrieved_context = retrieve_context(question)
    answer = generate_answer(question, retrieved_context)

    return {
        "question": question,
        "retrieved_context": retrieved_context,
        "answer": answer,
    }


if __name__ == "__main__":
    question = "What are the benefits of rooftop solar energy?"
    response = ask_question(question)

    print("Question")
    print(response["question"])
    print("\nRetrieved Context")

    if response["retrieved_context"]:
        for chunk in response["retrieved_context"]:
            print(f"- Source: {chunk['source']}")
            print(f"  {chunk['text']}\n")
    else:
        print("No relevant sustainability context was found.")

    print("Generated Answer")
    print(response["answer"])
    print("\n" + "=" * 50)
