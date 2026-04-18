"""Deterministic alignment scores derived from quiz scores + slider preferences."""
from __future__ import annotations

import math
from typing import Any

ARCHETYPE_KEYS = [
    "systems_thinker",
    "analytical_solver",
    "creative_builder",
    "people_strategist",
    "explorer",
    "impact_visionary",
]


def _clamp(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))


def _normalize_scores(scores: dict[str, Any] | None) -> list[float]:
    raw = []
    for key in ARCHETYPE_KEYS:
        v = scores.get(key) if isinstance(scores, dict) else None
        try:
            raw.append(float(v or 0))
        except (TypeError, ValueError):
            raw.append(0.0)
    m = max(raw) or 1.0
    return [x / m for x in raw]


def _slider_vector(sliders: dict[str, Any] | None) -> list[float]:
    s = sliders or {}
    try:
        structure = float(s.get("structure", 50))  # 0 flex — 100 structure
        analytical = float(s.get("analytical", 50))
        collaborative = float(s.get("collaborative", 50))  # 0 indep — 100 collab
        pace = float(s.get("pace", 50))  # 0 deep — 100 fast
    except (TypeError, ValueError):
        structure = analytical = collaborative = pace = 50.0
    structure = _clamp(structure, 0, 100) / 100.0
    analytical = _clamp(analytical, 0, 100) / 100.0
    collaborative = _clamp(collaborative, 0, 100) / 100.0
    pace = _clamp(pace, 0, 100) / 100.0
    flex_m = 1.0 - structure
    creative_m = 1.0 - analytical
    indep_m = 1.0 - collaborative
    deep_m = 1.0 - pace
    bias = [
        0.55 * structure + 0.15 * deep_m,
        0.5 * analytical + 0.25 * structure + 0.2 * deep_m,
        0.45 * creative_m + 0.2 * flex_m + 0.15 * pace,
        0.55 * collaborative + 0.2 * pace,
        0.45 * flex_m + 0.35 * pace + 0.15 * creative_m,
        0.4 * creative_m + 0.35 * deep_m + 0.2 * structure,
    ]
    return bias


def adjusted_profile_vector(scores: dict, sliders: dict | None) -> list[float]:
    base = _normalize_scores(scores)
    bias = _slider_vector(sliders)
    merged = [_clamp(base[i] * 0.72 + bias[i] * 0.55, 0.02, 1.4) for i in range(6)]
    norm = math.sqrt(sum(x * x for x in merged)) or 1.0
    return [x / norm for x in merged]


def _str_hash(s: str) -> int:
    """FNV-1a 32-bit — matches frontend/src/dashboard/personalize.js strHash."""
    h = 2166136261
    for c in s.encode("utf-8"):
        h ^= c
        h = (h * 16777619) & 0xFFFFFFFF
    return h


def _career_hint_vector(name: str) -> list[float]:
    """Stable pseudo-vector blended with lightweight keyword hints."""
    n = (name or "").lower()
    digest = _str_hash(f"career:{n}")
    base = [(((digest >> (i * 5)) & 31) / 31.0) * 0.35 + 0.1 for i in range(6)]
    hints = [0.0] * 6
    if any(k in n for k in ("data", "analyst", "finance", "engineer", "cs", "math", "stat")):
        hints[1] += 0.22
        hints[0] += 0.12
    if any(k in n for k in ("ux", "design", "product", "media", "art", "writer", "brand")):
        hints[2] += 0.22
        hints[4] += 0.08
    if any(k in n for k in ("psych", "hr", "people", "counsel", "social", "education", "nurse")):
        hints[3] += 0.22
    if any(k in n for k in ("policy", "nonprofit", "advocacy", "health", "community")):
        hints[5] += 0.18
        hints[3] += 0.1
    if any(k in n for k in ("ops", "supply", "logistics", "systems", "industrial")):
        hints[0] += 0.2
    if any(k in n for k in ("entrepreneur", "founder", "international", "explorer")):
        hints[4] += 0.18
    out = [_clamp(base[i] + hints[i], 0.05, 1.2) for i in range(6)]
    norm = math.sqrt(sum(x * x for x in out)) or 1.0
    return [x / norm for x in out]


def dot(a: list[float], b: list[float]) -> float:
    return sum(a[i] * b[i] for i in range(min(len(a), len(b))))


def alignment_score_0_100(user_vec: list[float], target_name: str) -> int:
    cvec = _career_hint_vector(target_name)
    d = dot(user_vec, cvec)
    raw = 58 + d * 38
    return int(_clamp(round(raw), 52, 96))


def compare_pathways(
    user_vec: list[float], items: list[str]
) -> list[dict[str, Any]]:
    rows = []
    for label in items:
        s = alignment_score_0_100(user_vec, label)
        cvec = _career_hint_vector(label)
        overlap = int(_clamp(round(dot(user_vec, cvec) * 100), 40, 95))
        rows.append(
            {
                "label": label,
                "alignment": s,
                "strength_overlap": overlap,
                "work_style_note": _work_style_diff(user_vec, cvec),
                "lifestyle_note": _lifestyle_note(user_vec, cvec),
            }
        )
    return rows


def _work_style_diff(u: list[float], c: list[float]) -> str:
    idx_u = max(range(6), key=lambda i: u[i])
    idx_c = max(range(6), key=lambda i: c[i])
    labels = ["systems", "analytical", "creative", "collaborative", "adaptive", "purpose-led"]
    if idx_u == idx_c:
        return f"Both lean {labels[idx_u]} — day-to-day decisions may feel familiar."
    return (
        f"You skew more {labels[idx_u]} while this path emphasizes {labels[idx_c]} work — "
        "worth sampling real projects in each style."
    )


def _lifestyle_note(u: list[float], c: list[float]) -> str:
    pace_signal = u[4] + u[3] * 0.35 - u[1] * 0.25
    deep_signal = u[1] + u[0] * 0.35 - u[4] * 0.2
    if pace_signal > deep_signal + 0.08:
        return "Likely more varied pacing and context switching than deep solo focus blocks."
    if deep_signal > pace_signal + 0.08:
        return "Likely more sustained focus blocks and fewer rapid context shifts."
    return "Balanced between focused stretches and collaborative touchpoints."
