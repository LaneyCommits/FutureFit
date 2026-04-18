from __future__ import annotations

import re
from typing import Any

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from . import ai_service, fallbacks, scoring

VOICE = (
    "You write short copy for a student career dashboard called ExploringU. "
    "Tone: supportive, clear, not clinical or therapy-speak. Avoid repeating the same opening phrase. "
    "Do not invent biographical facts. Ground statements in the JSON profile only."
)


def _profile_from_request(data: dict) -> dict:
    return data.get("profile") or {}


def _sliders(data: dict) -> dict | None:
    s = data.get("sliders")
    return s if isinstance(s, dict) else None


def _merge_compare_rows(
    gemini_rows: list[Any], base_rows: list[dict[str, Any]], items: list[str]
) -> list[dict[str, Any]]:
    merged = []

    def _int(value: Any, default: int) -> int:
        try:
            return int(value)
        except (TypeError, ValueError):
            return default

    for i, label in enumerate(items):
        g = gemini_rows[i] if i < len(gemini_rows) and isinstance(gemini_rows[i], dict) else {}
        b = base_rows[i]
        merged.append(
            {
                "label": str(g.get("label") or label)[:120],
                "alignment": _int(g.get("alignment"), b["alignment"]),
                "strength_overlap": _int(
                    g.get("strength_overlap") or g.get("strengthOverlap"),
                    b["strength_overlap"],
                ),
                "work_style_note": str(
                    g.get("work_style_note") or g.get("workStyleNote") or b["work_style_note"]
                )[:400],
                "lifestyle_note": str(
                    g.get("lifestyle_note") or g.get("lifestyleNote") or b["lifestyle_note"]
                )[:400],
            }
        )
    return merged


def _sanitize_items(items: list[Any], max_n: int = 3) -> list[str]:
    out = []
    for x in items or []:
        if not isinstance(x, str):
            continue
        t = re.sub(r"\s+", " ", x).strip()
        if not t or len(t) > 120:
            continue
        if t not in out:
            out.append(t)
        if len(out) >= max_n:
            break
    return out


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def today_insight_view(request):
    data = request.data if isinstance(request.data, dict) else {}
    profile = _profile_from_request(data)
    sliders = _sliders(data)
    rotation = str(data.get("rotation_key") or request.user.id)
    prompt = (
        f"{VOICE}\nWrite exactly 1-2 sentences (max 320 characters).\n"
        f"rotation_key={rotation!r} (use to vary wording).\n"
        f"profile={profile!s}\npreferences={sliders!s}\n"
        "Give one actionable insight connecting strengths to exploration."
    )
    raw_ai = ai_service.generate_text(prompt, temperature=0.75)
    if raw_ai and len(raw_ai) <= 650:
        text = raw_ai.strip()
        source = "gemini"
    else:
        text = fallbacks.today_insight(profile, sliders, str(rotation))
        source = "fallback"
    if len(text) > 420:
        text = text[:417].rsplit(" ", 1)[0] + "…"
    return Response({"text": text, "source": source})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def career_match_view(request):
    data = request.data if isinstance(request.data, dict) else {}
    profile = _profile_from_request(data)
    sliders = _sliders(data)
    target = (data.get("target") or data.get("career") or "").strip()
    kind = (data.get("kind") or "career").strip().lower()
    if not target:
        return Response({"error": "target is required."}, status=status.HTTP_400_BAD_REQUEST)

    user_vec = scoring.adjusted_profile_vector(profile.get("scores") or {}, sliders)
    score = scoring.alignment_score_0_100(user_vec, target)

    prompt = (
        f"{VOICE}\nReturn JSON with keys: why_fit (string, 1-2 sentences), "
        f"challenges (string, 1 sentence), alternatives (array of 2-3 short career/major names).\n"
        f"kind={kind!r} target={target!r}\nprofile={profile!s}\nsliders={sliders!s}\n"
        f"The student's deterministic fit score is {score} (you may reference it subtly, do not contradict wildly)."
    )
    parsed = ai_service.generate_json_object(prompt, temperature=0.55)
    if isinstance(parsed, dict) and parsed.get("why_fit"):
        return Response(
            {
                "score": score,
                "why_fit": str(parsed.get("why_fit", "")).strip(),
                "challenges": str(parsed.get("challenges", "")).strip(),
                "alternatives": [str(x) for x in (parsed.get("alternatives") or []) if x][:3],
                "source": "gemini",
            }
        )
    fb = fallbacks.career_match_copy(profile, sliders, target, kind)
    fb["score"] = score
    return Response(fb)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def compare_view(request):
    data = request.data if isinstance(request.data, dict) else {}
    profile = _profile_from_request(data)
    sliders = _sliders(data)
    raw_items = data.get("items") or data.get("careers") or []
    items = _sanitize_items(raw_items if isinstance(raw_items, list) else [], max_n=3)
    if len(items) < 2:
        return Response(
            {"error": "Provide 2-3 pathway names in items[]."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user_vec = scoring.adjusted_profile_vector(profile.get("scores") or {}, sliders)
    base_rows = scoring.compare_pathways(user_vec, items)

    prompt = (
        f"{VOICE}\nReturn JSON: narrative (1-2 sentences), rows (array of same length as items, "
        "each object: label, alignment (int 52-96), strength_overlap (int 40-95), "
        "work_style_note (short), lifestyle_note (short)). Must align labels to this order: "
        f"{items!s}. Use profile={profile!s} sliders={sliders!s}. "
        f"Numerical fields should be close to: {base_rows!s}"
    )
    parsed = ai_service.generate_json_object(prompt, temperature=0.4)
    if isinstance(parsed, dict) and isinstance(parsed.get("rows"), list) and len(parsed["rows"]) == len(items):
        rows = _merge_compare_rows(parsed["rows"], base_rows, items)
        return Response(
            {
                "rows": rows,
                "narrative": str(parsed.get("narrative", "")).strip(),
                "source": "gemini",
            }
        )
    return Response(fallbacks.compare_fallback(items, profile, sliders))


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def saved_pattern_view(request):
    data = request.data if isinstance(request.data, dict) else {}
    profile = _profile_from_request(data)
    raw = data.get("saved") or []
    saved = [str(x).strip() for x in raw if isinstance(x, str) and str(x).strip()][:24]

    prompt = (
        f"{VOICE}\nReturn JSON keys: summary (one short sentence listing theme), "
        f"insight (one sentence connecting pattern to profile).\n"
        f"saved={saved!s}\nprofile={profile!s}"
    )
    parsed = ai_service.generate_json_object(prompt, temperature=0.55)
    if isinstance(parsed, dict) and parsed.get("insight"):
        return Response(
            {
                "summary": str(parsed.get("summary", "")).strip(),
                "insight": str(parsed.get("insight", "")).strip(),
                "source": "gemini",
            }
        )
    return Response(fallbacks.saved_pattern_insight(saved, profile))


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def weekly_reflection_view(request):
    data = request.data if isinstance(request.data, dict) else {}
    profile = _profile_from_request(data)
    acts = data.get("activities") or []
    if not isinstance(acts, list):
        acts = []

    prompt = (
        f"{VOICE}\nWrite 1-2 sentences summarizing this week's exploration, warm and specific.\n"
        f"activities={acts!s}\nprofile={profile!s}"
    )
    text = ai_service.generate_text(prompt, temperature=0.65)
    if not text:
        text = fallbacks.weekly_reflection(acts, profile)
    text = text.strip()
    if len(text) > 500:
        text = text[:497].rsplit(" ", 1)[0] + "…"
    return Response({"text": text, "source": "gemini" if text else "fallback"})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def career_feed_view(request):
    data = request.data if isinstance(request.data, dict) else {}
    profile = _profile_from_request(data)
    sliders = _sliders(data)
    raw = data.get("careers") or []
    careers = [str(x).strip() for x in raw if isinstance(x, str) and str(x).strip()][:12]
    if not careers:
        return Response({"error": "careers[] is required."}, status=status.HTTP_400_BAD_REQUEST)

    prompt = (
        f"{VOICE}\nReturn JSON: cards array; each card: name, short_description (max 220 chars), "
        f"why_fit (max 200 chars). careers in order: {careers!s}\nprofile={profile!s}\nsliders={sliders!s}"
    )
    parsed = ai_service.generate_json_object(prompt, temperature=0.55)
    if isinstance(parsed, dict):
        cards = parsed.get("cards")
        if isinstance(cards, list) and len(cards) >= min(3, len(careers)):
            return Response({"cards": cards, "source": "gemini"})
    return Response({"cards": fallbacks.career_feed_fallback(careers, profile, sliders), "source": "fallback"})
