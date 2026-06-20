# EcoGen AI - Session 8 Requirements

## Session Name

RAG Sustainability Assistant

---

# Objective

Build a Retrieval-Augmented Generation (RAG) Sustainability Assistant capable of answering sustainability questions using trusted knowledge documents.

Current System:

User
↓
Carbon Calculator
↓
Prediction Engine
↓
Explainability Engine
↓
Recommendation Engine
↓
Location Intelligence
↓
GenAI Sustainability Advisor

Problem:

The system can generate advice but cannot answer sustainability questions using external knowledge.

Example:

User asks:

"What are the benefits of rooftop solar energy?"

Current System:

Cannot answer.

Session 8 solves this problem.

---

# Session 8 Goal

Move from:

Static Sustainability Advisor

to:

Interactive Sustainability Knowledge Assistant

---

# Module Structure

rag/

├── documents/
│
├── ingestion/
│   └── ingest.py
│
├── vectorstore/
│   └── faiss_index/
│
└── chatbot/
└── rag_assistant.py

---

# Knowledge Sources

Store documents in:

rag/documents/

Create folders:

* sdg/
* policies/
* climate_reports/
* renewable_energy/

Documents may be:

* TXT
* PDF
* Markdown

---

# RAG Pipeline

Document
↓
Chunking
↓
Embedding Generation
↓
FAISS Vector Store
↓
Similarity Search
↓
Context Retrieval
↓
Answer Generation

---

# Session Components

## Component 1

Document Ingestion

File:

rag/ingestion/ingest.py

Responsibilities:

* Load documents
* Read text
* Chunk documents
* Prepare embeddings

---

## Component 2

Vector Store

Directory:

rag/vectorstore/faiss_index/

Responsibilities:

* Store embeddings
* Similarity search
* Retrieve relevant chunks

---

## Component 3

RAG Assistant

File:

rag/chatbot/rag_assistant.py

Responsibilities:

* Accept user query
* Search vector store
* Retrieve relevant chunks
* Generate grounded answer

---

# Embedding Model

Use:

sentence-transformers

Recommended:

all-MiniLM-L6-v2

---

# Vector Database

Use:

FAISS

---

# Required Functions

## ingest.py

load_documents()

chunk_documents()

generate_embeddings()

build_vector_store()

---

## rag_assistant.py

load_vector_store()

retrieve_context()

generate_answer()

ask_question()

---

# Example Questions

What are the benefits of solar energy?

How can households reduce carbon emissions?

What is SDG 13?

How does rainwater harvesting help sustainability?

What are India's renewable energy goals?

---

# Example Output

Question:

What are the benefits of solar energy?

Retrieved Context:

Solar energy reduces dependence on fossil fuels and lowers greenhouse gas emissions.

Answer:

Solar energy provides clean renewable power, reduces carbon emissions, lowers electricity costs over time, and supports long-term sustainability goals.

---

# Output Format

{
"question": "",
"retrieved_context": [],
"answer": ""
}

---

# Demo Mode

if **name** == "**main**":

Question:

What are the benefits of rooftop solar energy?

Print:

==================================================
ECOGEN AI - RAG ASSISTANT
=========================

Question

Retrieved Context

Generated Answer

==================================================

---

# Success Criteria

User asks a sustainability question.

System:

1. Retrieves relevant document chunks.
2. Uses retrieved content.
3. Generates grounded answer.
4. Returns answer with context.

---

# Constraints

Do Not Modify:

* ml/
* database/
* genai/

Only Work In:

* rag/

---

# Deliverables

1. Document Ingestion Pipeline
2. Embedding Generation
3. FAISS Vector Store
4. Retrieval System
5. Sustainability Assistant
6. RAG Testing

Session 8 is complete only when EcoGen AI can answer sustainability questions using retrieved knowledge rather than hardcoded responses.
