"""Placeholder LLM interface."""

from pathlib import Path
from duckduckgo_search import DDGS


def load_model(path: str | None = None):
    path = path or Path('./model')
    # In production, load the fine-tuned model here
    return {'path': str(path)}


def web_search(query: str) -> str:
    """Return short snippet from web search."""
    with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results=1))
    if results:
        return results[0].get("body", "")
    return ""


def generate_answer(model, query: str) -> str:
    """Generate answer from the model (dummy implementation)."""
    answer = f"[Answer based on {model['path']}] {query}"
    search_snippet = web_search(query)
    if search_snippet:
        answer += f"\n\nWeb result: {search_snippet}"
    return answer
