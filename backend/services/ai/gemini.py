"""
Deprecated shim for backwards compatibility.

Gemini has been replaced by Meta Spark 1.1. This module re-exports the
Meta Spark implementation so existing imports (`services.ai.gemini`) keep working.
New code should import from `services.ai.spark`.
"""
import warnings

warnings.warn(
    "services.ai.gemini is deprecated, use services.ai.spark (Meta Spark 1.1) instead.",
    DeprecationWarning,
    stacklevel=2,
)

from .spark import ai_service, AIService  # noqa: F401

# Backwards compat aliases
from .spark import SPARK_API_KEY as GEMINI_KEY  # noqa: F401
from .spark import MODEL_API_KEY  # noqa: F401
