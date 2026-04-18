"""Optional Gemini generation for dashboard insights (server-side key)."""
from __future__ import annotations

import json
import logging
import os
import re

logger = logging.getLogger(__name__)


def _get_api_key() -> str | None:
    return (os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY") or "").strip() or None


def generate_text(prompt: str, *, temperature: float = 0.65) -> str | None:
    key = _get_api_key()
    if not key:
        return None
    try:
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=key)
        model_name = os.environ.get("GEMINI_MODEL", "gemini-3-flash-preview")
        config = types.GenerateContentConfig(
            temperature=temperature,
            max_output_tokens=768,
        )
        resp = client.models.generate_content(
            model=model_name,
            contents=prompt,
            config=config,
        )
        text = (getattr(resp, "text", None) or "").strip()
        return text or None
    except Exception:
        logger.exception("Gemini generate_text failed")
        return None


def generate_json_object(prompt: str, *, temperature: float = 0.45) -> dict | None:
    text = generate_text(
        prompt
        + "\n\nRespond with a single valid JSON object only. No markdown fences, no commentary.",
        temperature=temperature,
    )
    if not text:
        return None
    cleaned = text.strip()
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s*```$", "", cleaned)
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        logger.warning("Gemini JSON parse failed: %s", cleaned[:200])
        return None
