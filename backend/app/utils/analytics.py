"""Optional analytics hooks."""

import os
import logging

ENABLED = os.environ.get("ANALYTICS_ENABLED", "false").lower() == "true"
logger = logging.getLogger("analytics")

if ENABLED:
    handler = logging.FileHandler("analytics.log")
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)


def log_event(event: str, data: dict | None = None) -> None:
    """Log an analytics event if enabled."""
    if not ENABLED:
        return
    logger.info("%s:%s", event, data or {})
