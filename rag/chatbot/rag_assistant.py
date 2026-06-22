"""Retrieval-Augmented Generation (RAG) assistant logic.

This module keeps the retrieval pipeline separate from the Streamlit UI and
connects retrieved document chunks with grounded Gemini responses.
"""

from __future__ import annotations

from typing import Any, Dict, List

import numpy as np
from sentence_transformers import SentenceTransformer

from chatbot.sustainability_advisor import get_gemini_response
from rag.ingestion.ingest import load_vector_store as load_indexed_chunks

ContextChunk = Dict[str, Any]
AnswerPackage = Dict[str, Any]

MODEL_NAME = "all-MiniLM-L6-v2"
_EMBEDDER: SentenceTransformer | None = None


def _get_embedder() -> SentenceTransformer:
    """Load the sentence transformer model once and reuse it."""
    global _EMBEDDER
    if _EMBEDDER is None:
        _EMBEDDER = SentenceTransformer(MODEL_NAME)
    return _EMBEDDER


def _embed_question(question: str) -> np.ndarray:
    """Embed a question using the sentence transformer model."""
    model = _get_embedder()
    embedding = model.encode([question], show_progress_bar=False, convert_to_numpy=True)

    if embedding.ndim != 2:
        raise ValueError("Unexpected embedding shape from sentence-transformer model.")

    return embedding.astype("float32")


def _normalize_score(distance: float) -> float:
    """Convert FAISS distance into a confidence-like score between 0 and 1."""
    if distance is None:
        return 0.0
    score = 1.0 / (1.0 + max(0.0, float(distance)))
    return round(max(0.0, min(1.0, score)), 4)


def _format_context_chunk(chunk: Dict[str, Any], rank: int) -> Dict[str, Any]:
    text = str(chunk.get("text", "")).strip()
    if not text:
        return {}

    source = str(chunk.get("source", "unknown"))
    title = str(chunk.get("title", source.split("/")[-1]))

    return {
        "rank": rank,
        "text": text,
        "source": source,
        "title": title,
        "score": chunk.get("score", 0.0),
    }


def retrieve_context(question: str, top_k: int = 5) -> List[ContextChunk]:
    """Retrieve the top matching document chunks for a question using FAISS."""

    if not isinstance(question, str):
        raise TypeError("Question must be a string.")
    if not question.strip():
        return []
    if not isinstance(top_k, int) or top_k <= 0:
        raise ValueError("top_k must be a positive integer.")

    try:
        index, chunks = load_indexed_chunks()
    except Exception as exc:
        raise RuntimeError(f"Unable to load knowledge base: {exc}") from exc

    question_embedding = _embed_question(question)
    distances, indices = index.search(question_embedding, top_k)

    context_chunks: List[ContextChunk] = []

    for rank, idx in enumerate(indices[0], start=1):
        if idx < 0 or idx >= len(chunks):
            continue

        chunk = chunks[int(idx)]
        if not isinstance(chunk, dict):
            continue

        text = str(chunk.get("text", "")).strip()
        if not text:
            continue

        score = _normalize_score(float(distances[0][rank - 1]) if rank - 1 < len(distances[0]) else 0.0)
        formatted_chunk = _format_context_chunk(
            {
                **chunk,
                "score": score,
            },
            rank,
        )
        if formatted_chunk:
            context_chunks.append(formatted_chunk)

    return context_chunks


def build_grounded_prompt(question: str, context: List[ContextChunk]) -> str:
    """Build a prompt that grounds Gemini answers in retrieved knowledge."""
    if not context:
        return (
            f"You are EcoGen AI. The user asked: {question}\n"
            "No relevant sustainability context was retrieved. "
            "Respond briefly and honestly that the knowledge base does not contain enough information."
        )

    citations = "\n".join(
        f"- {chunk.get('title', 'Source')} ({chunk.get('source', 'unknown')})\n  {chunk.get('text', '')}"
        for chunk in context[:5]
    )

    return f"""
You are EcoGen AI's Sustainability Knowledge Assistant.
Use ONLY the retrieved knowledge below to answer the user's question.
If the answer is not supported by the context, say that the information is not available in the knowledge base.
Do not invent facts.

User Question:
{question}

Retrieved Knowledge Context:
{citations}

Instructions:
1. Answer in plain language.
2. Mention the most relevant sources using the exact source path shown above.
3. If possible, include a short confidence note based on how directly the context matches the question.
4. Keep the response concise but helpful.
"""


def generate_answer(question: str, context: List[ContextChunk]) -> str:
    """Generate a grounded answer using the retrieved context."""
    if not isinstance(question, str) or not question.strip():
        raise ValueError("Question cannot be empty.")

    if not context:
        return (
            "I couldn't find enough relevant sustainability information in the current knowledge base. "
            "Please try a different question or reindex the documents."
        )

    prompt = build_grounded_prompt(question, context)

    try:
        raw_response = get_gemini_response(prompt)
        return raw_response.strip()
    except Exception:
        # Fallback to a context-based response when Gemini is unavailable.
        top_chunks = context[:3]
        evidence = "\n\n".join(
            f"Source: {chunk.get('source', 'unknown')}\n{chunk.get('text', '')}"
            for chunk in top_chunks
        )
        return (
            "I could not reach the Gemini service, so here is a grounded summary from the retrieved documents:\n\n"
            f"{evidence}"
        )


def ask_question(question: str) -> AnswerPackage:
    """Ask a sustainability question and return the retrieved context and answer."""
    if not isinstance(question, str):
        raise TypeError("Question must be a string.")
    if not question.strip():
        raise ValueError("Question cannot be empty.")

    retrieved_context = retrieve_context(question)
    answer = generate_answer(question, retrieved_context)
    confidence = round(
        sum(chunk.get("score", 0.0) for chunk in retrieved_context) / len(retrieved_context), 2
    ) if retrieved_context else 0.0

    return {
        "question": question,
        "retrieved_context": retrieved_context,
        "answer": answer,
        "confidence": confidence,
        "sources": [chunk.get("source", "unknown") for chunk in retrieved_context],
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
    print("\nConfidence:")
    print(response["confidence"])
    print("\n" + "=" * 50)
