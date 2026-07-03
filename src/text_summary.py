"""
Caption-to-summary helper.

Uses a Hugging Face summarization pipeline when available and falls back to
simple deterministic shortening when model loading is unavailable.
"""

from __future__ import annotations

import logging
import re


logger = logging.getLogger(__name__)


class TextSummarizer:
    """Generate short summaries from caption text."""

    def __init__(
        self,
        model_name: str = "sshleifer/distilbart-cnn-12-6",
        max_length: int = 40,
        min_length: int = 10,
    ):
        self.model_name = model_name
        self.max_length = max_length
        self.min_length = min_length

        self._pipeline = None
        self._load_attempted = False

    def _get_pipeline(self):

        if self._load_attempted:
            return self._pipeline

        self._load_attempted = True

        try:
            from transformers import pipeline

            self._pipeline = pipeline("summarization", model=self.model_name)

        except Exception as error:
            logger.warning("Falling back to rule-based summary generation: %s", error)
            self._pipeline = None

        return self._pipeline

    @staticmethod
    def _clean(text: str) -> str:
        return re.sub(r"\s+", " ", text or "").strip()

    def _fallback_summary(self, text: str) -> str:

        normalized = self._clean(text)
        if not normalized:
            return "No scene summary available."

        if len(normalized) <= 90:
            if normalized[-1] in {".", "!", "?"}:
                return normalized
            return f"{normalized}."

        separators = [". ", "; ", ", while ", " while ", ", and ", " and "]

        for separator in separators:
            if separator in normalized:
                head = normalized.split(separator, 1)[0].strip(" ,;:")
                if len(head) >= 20:
                    if head.endswith((".", "!", "?")):
                        return head
                    return f"{head}."

        shortened = normalized[:87].rstrip(" ,;:")
        return f"{shortened}..."

    def generate_summary(
        self,
        text: str,
        max_length: int | None = None,
        min_length: int | None = None,
    ) -> str:

        normalized = self._clean(text)
        if not normalized:
            return "No scene summary available."

        summarizer = self._get_pipeline()
        if summarizer is None:
            return self._fallback_summary(normalized)

        target_max = max_length if max_length is not None else self.max_length
        target_min = min_length if min_length is not None else self.min_length
        if target_min >= target_max:
            target_min = max(5, target_max - 5)

        try:
            result = summarizer(
                normalized,
                max_length=target_max,
                min_length=target_min,
                do_sample=False,
                truncation=True,
            )

            if result and isinstance(result, list):
                candidate = self._clean(result[0].get("summary_text", ""))
                if candidate:
                    return candidate

        except Exception as error:
            logger.warning("Transformer summarization failed, using fallback: %s", error)

        return self._fallback_summary(normalized)


_default_summarizer = TextSummarizer()


def generate_summary(text: str) -> str:
    """Module-level helper for one-off caption summarization."""

    return _default_summarizer.generate_summary(text)
