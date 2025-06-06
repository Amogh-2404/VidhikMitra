"""Security utilities for redacting personal identifiers."""

import re

REDACTION_PATTERNS = [
    r'\b\d{12}\b',  # Aadhaar
    r'[A-Z]{5}\d{4}[A-Z]',  # PAN
    r'\b\d{10}\b',  # phone
]


def redact(text: str) -> str:
    """Redact sensitive patterns."""
    for pattern in REDACTION_PATTERNS:
        text = re.sub(pattern, '[REDACTED]', text)
    return text
