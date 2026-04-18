"""Rule-based copy when Gemini is unavailable or fails."""
from __future__ import annotations

import hashlib
from typing import Any

from . import scoring

ARCHETYPE_LABELS = {
    "systems_thinker": "structured systems thinking",
    "analytical_solver": "analytical problem-solving",
    "creative_builder": "creative building and iteration",
    "people_strategist": "people-centered strategy",
    "explorer": "adaptive exploration",
    "impact_visionary": "purpose-led vision",
}


def _hash_seed(*parts: str) -> int:
    h = hashlib.sha256("|".join(parts).encode("utf-8")).digest()
    return int.from_bytes(h[:4], "big")


def today_insight(profile: dict, sliders: dict | None, rotation: str) -> str:
    pk = profile.get("primary_key") or "systems_thinker"
    pname = profile.get("primary_name") or "Your profile"
    label = ARCHETYPE_LABELS.get(pk, "your decision strengths")
    seed = _hash_seed(rotation, pk, str((sliders or {}).get("structure", 50)))
    variants = [
        f"Your strongest signal is {label}. Leaning into courses and projects that reward clarity, feedback loops, and measurable progress will feel most natural right now.",
        f"With {pname} as your lead pattern, environments that respect {label} tend to sustain your motivation longer than purely open-ended work without checkpoints.",
        f"You show a clear tilt toward {label}. Pair that strength with one stretch experience this month that adds a complementary skill so options stay wide.",
        f"Because {label} shows up strongly for you, look for roles where your thinking style is the main engine of the work—not a side note.",
        f"Your profile reads as {label}-forward. Shortlist paths where you can see how your contributions connect to outcomes within a semester, not only years out.",
    ]
    return variants[seed % len(variants)]


def career_match_copy(
    profile: dict, sliders: dict | None, target: str, kind: str
) -> dict[str, Any]:
    user_vec = scoring.adjusted_profile_vector(profile.get("scores") or {}, sliders)
    score = scoring.alignment_score_0_100(user_vec, target)
    pk = profile.get("primary_key") or "systems_thinker"
    seed = _hash_seed(target, pk, str(score))
    why = [
        f"This aligns with your {ARCHETYPE_LABELS.get(pk, 'profile')} tendencies. The day-to-day work may feel engaging when problems are concrete and progress is visible.",
        f"Given your lead style, {target} can reward how you like to think—especially when you can iterate with feedback rather than guessing in isolation.",
        f"You may enjoy how {target} connects pattern recognition with real decisions; it tends to fit learners who like both structure and momentum.",
    ][seed % 3]
    challenges = [
        "Some stretches may feel abstract or slow until you build domain intuition—plan early wins to stay motivated.",
        "You might need to adapt when priorities shift quickly; anchor on one measurable skill per season.",
        "If collaboration load is uneven, clarify roles early so your energy goes to the problems you care about most.",
    ][(seed + 1) % 3]
    alts = _alternatives(target, seed)
    return {
        "score": score,
        "why_fit": why,
        "challenges": challenges,
        "alternatives": alts,
        "source": "fallback",
    }


def _alternatives(target: str, seed: int) -> list[str]:
    pool = [
        "Product Operations",
        "UX Research",
        "Business Analytics",
        "Program Management",
        "Technical Writing",
        "Community Strategy",
    ]
    tlow = target.lower()
    filtered = [p for p in pool if p.lower() not in tlow]
    out = []
    i = seed % max(len(filtered), 1)
    for _ in range(3):
        if not filtered:
            break
        out.append(filtered[i % len(filtered)])
        i += 2
    return out or pool[:3]


def saved_pattern_insight(saved: list[str], profile: dict) -> dict[str, str]:
    if not saved:
        return {
            "summary": "Save a few careers or majors to see patterns across your interests.",
            "insight": "When you bookmark paths, we can highlight recurring themes in how you like to work and decide.",
        }
    joined = ", ".join(saved[:6])
    pk = profile.get("primary_key") or "systems_thinker"
    seed = _hash_seed(joined, pk)
    themes = [
        "structured problem-solving with visible outcomes",
        "roles that blend human insight with practical delivery",
        "paths where curiosity and craft both matter",
    ]
    theme = themes[seed % len(themes)]
    return {
        "summary": f"You saved: {joined}.",
        "insight": f"So far you lean toward {theme}, which fits how your {ARCHETYPE_LABELS.get(pk, 'profile')} pattern shows up.",
    }


def weekly_reflection(activities: list[dict], profile: dict) -> str:
    if not activities:
        return (
            "This week, try exploring two different directions—even briefly—so your next reflection "
            "has contrast to learn from."
        )
    names = [a.get("name", "a pathway") for a in activities if isinstance(a, dict)]
    uniq = []
    for n in names:
        if n and n not in uniq:
            uniq.append(n)
    sample = uniq[:4]
    pk = profile.get("primary_key") or "systems_thinker"
    if len(sample) == 1:
        return (
            f"This week you focused on {sample[0]}. Notice what parts felt energizing versus draining—"
            f"that contrast is useful signal for your {ARCHETYPE_LABELS.get(pk, 'style')} strengths."
        )
    return (
        f"This week you explored {', '.join(sample)}. Both sit in different corners of the map, "
        "which helps you separate what you like from what sounds impressive on paper."
    )


def career_feed_fallback(careers: list[str], profile: dict, sliders: dict | None) -> list[dict]:
    user_vec = scoring.adjusted_profile_vector(profile.get("scores") or {}, sliders)
    pk = profile.get("primary_key") or "systems_thinker"
    out = []
    for i, title in enumerate(careers):
        seed = _hash_seed(title, pk, str(i))
        score = scoring.alignment_score_0_100(user_vec, title)
        desc = [
            f"A pathway where {title.lower()} work rewards your {ARCHETYPE_LABELS.get(pk, 'natural strengths')} without forcing you into a generic mold.",
            f"{title} often mixes tangible deliverables with learning curves that stay interesting for your decision style.",
            f"If you like progress you can point to, {title} can give you milestones while still leaving room to grow.",
        ][seed % 3]
        why = f"Estimated fit around {score}% based on your profile and slider preferences—not a verdict, just a compass."
        out.append({"name": title, "short_description": desc, "why_fit": why})
    return out


def compare_fallback(items: list[str], profile: dict, sliders: dict | None) -> dict[str, Any]:
    user_vec = scoring.adjusted_profile_vector(profile.get("scores") or {}, sliders)
    rows = scoring.compare_pathways(user_vec, items)
    seed = _hash_seed(*items, str(profile.get("primary_key", "")))
    narrative = [
        "Side-by-side, the biggest difference is where each path spends its cognitive energy day to day.",
        "Use this comparison to choose experiments, not a final label—short exposures beat long guessing.",
        "Look for which option gives you more chances to practice the strengths you want to grow, not only what fits today.",
    ][seed % 3]
    return {"rows": rows, "narrative": narrative, "source": "fallback"}
