"""Document question answering utilities."""

from functools import lru_cache
from transformers import pipeline


@lru_cache(maxsize=1)
def get_qa_pipeline():
    """Load QA pipeline lazily."""
    try:
        return pipeline("question-answering", model="deepset/roberta-base-squad2")
    except Exception:
        return None


def answer_question(context: str, question: str) -> str:
    """Return answer given context using QA model."""
    qa = get_qa_pipeline()
    if qa is None:
        # Fallback: simple heuristic if model unavailable
        return context[:200]
    try:
        result = qa(question=question, context=context)
        return result.get("answer", "")
    except Exception:
        return ""
