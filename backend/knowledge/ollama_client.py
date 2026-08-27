"""Thin HTTP client for a local Ollama server (no API key needed)."""

import requests
from django.conf import settings


def embed(text: str) -> list[float]:
    response = requests.post(
        f"{settings.OLLAMA_BASE_URL}/api/embeddings",
        json={"model": settings.OLLAMA_EMBED_MODEL, "prompt": text},
        timeout=60,
    )
    response.raise_for_status()
    return response.json()["embedding"]


def chat(messages: list[dict]) -> str:
    """messages: [{"role": "system"|"user"|"assistant", "content": str}, ...]"""
    response = requests.post(
        f"{settings.OLLAMA_BASE_URL}/api/chat",
        json={"model": settings.OLLAMA_CHAT_MODEL, "messages": messages, "stream": False},
        timeout=120,
    )
    response.raise_for_status()
    return response.json()["message"]["content"]
