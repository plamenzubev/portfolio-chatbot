# Contract Assistant

A local-first RAG application: upload a contract (PDF or DOCX) and ask natural language
questions about it. Answers are grounded exclusively in the uploaded document, with
clickable citations linking back to the exact source passage, so it never hallucinates
facts not in the contract.

Key features: grounded, cited answers; real-time token-by-token streaming of the
response; the document is queryable immediately after upload; session-based chat
history.

Tech stack: Django + Django REST Framework backend, PostgreSQL 17 with the pgvector
extension for vector search, Ollama for local LLM inference (llama3.1:8b for answers,
nomic-embed-text for embeddings), React + Vite frontend. Document parsing uses
pdfplumber and python-docx. Text is recursively chunked (~800 characters) before
embedding and semantic search via cosine similarity.

The whole system runs entirely locally with no cloud API keys and no per-token cost.
GitHub: https://github.com/plamenzubev/contract-assistant
