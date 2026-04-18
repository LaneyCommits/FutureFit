/**
 * Deterministic profile adjustments — keep in sync with apps/insights/scoring.py
 */
const ARCHETYPE_KEYS = [
  "systems_thinker",
  "analytical_solver",
  "creative_builder",
  "people_strategist",
  "explorer",
  "impact_visionary",
];

function clamp(x, lo, hi) {
  return Math.max(lo, Math.min(hi, x));
}

function normalizeScoresObject(scores) {
  const raw = ARCHETYPE_KEYS.map((k) => {
    const v = scores?.[k];
    const n = Number(v);
    return Number.isFinite(n) ? n : 0;
  });
  const m = Math.max(...raw, 1);
  return raw.map((x) => x / m);
}

function sliderVector(sliders) {
  const s = sliders || {};
  const structure = clamp(Number(s.structure ?? 50), 0, 100) / 100;
  const analytical = clamp(Number(s.analytical ?? 50), 0, 100) / 100;
  const collaborative = clamp(Number(s.collaborative ?? 50), 0, 100) / 100;
  const pace = clamp(Number(s.pace ?? 50), 0, 100) / 100;
  const flexM = 1 - structure;
  const creativeM = 1 - analytical;
  const indepM = 1 - collaborative;
  const deepM = 1 - pace;
  return [
    0.55 * structure + 0.15 * deepM,
    0.5 * analytical + 0.25 * structure + 0.2 * deepM,
    0.45 * creativeM + 0.2 * flexM + 0.15 * pace,
    0.55 * collaborative + 0.2 * pace,
    0.45 * flexM + 0.35 * pace + 0.15 * creativeM,
    0.4 * creativeM + 0.35 * deepM + 0.2 * structure,
  ];
}

function adjustedProfileVector(scoresObj, sliders) {
  const base = normalizeScoresObject(scoresObj || {});
  const bias = sliderVector(sliders);
  const merged = base.map((b, i) => clamp(b * 0.72 + bias[i] * 0.55, 0.02, 1.4));
  const norm = Math.sqrt(merged.reduce((a, x) => a + x * x, 0)) || 1;
  return merged.map((x) => x / norm);
}

function strHash(s) {
  let h = 2166136261;
  for (let i = 0; i < s.length; i += 1) {
    h ^= s.charCodeAt(i);
    h = Math.imul(h, 16777619);
  }
  return h >>> 0;
}

function careerHintVector(name) {
  const n = String(name || "").toLowerCase();
  const digest = strHash(`career:${n}`);
  const base = ARCHETYPE_KEYS.map((_, i) => (((digest >> (i * 5)) & 31) / 31) * 0.35 + 0.1);
  const hints = [0, 0, 0, 0, 0, 0];
  if (/data|analyst|finance|engineer|cs|math|stat/.test(n)) {
    hints[1] += 0.22;
    hints[0] += 0.12;
  }
  if (/ux|design|product|media|art|writer|brand/.test(n)) {
    hints[2] += 0.22;
    hints[4] += 0.08;
  }
  if (/psych|hr|people|counsel|social|education|nurse/.test(n)) hints[3] += 0.22;
  if (/policy|nonprofit|advocacy|health|community/.test(n)) {
    hints[5] += 0.18;
    hints[3] += 0.1;
  }
  if (/ops|supply|logistics|systems|industrial/.test(n)) hints[0] += 0.2;
  if (/entrepreneur|founder|international|explorer/.test(n)) hints[4] += 0.18;
  const out = base.map((b, i) => clamp(b + hints[i], 0.05, 1.2));
  const norm = Math.sqrt(out.reduce((a, x) => a + x * x, 0)) || 1;
  return out.map((x) => x / norm);
}

function dot(a, b) {
  return a.reduce((s, x, i) => s + x * b[i], 0);
}

export function alignmentScore0to100(scoresObj, sliders, targetName) {
  const u = adjustedProfileVector(scoresObj, sliders);
  const c = careerHintVector(targetName);
  const d = dot(u, c);
  const raw = 58 + d * 38;
  return Math.round(clamp(raw, 52, 96));
}

export function comparePathwayRows(scoresObj, sliders, items) {
  const u = adjustedProfileVector(scoresObj, sliders);
  const labels = ["systems", "analytical", "creative", "collaborative", "adaptive", "purpose-led"];
  return items.map((label) => {
    const c = careerHintVector(label);
    const alignment = alignmentScore0to100(scoresObj, sliders, label);
    const overlap = Math.round(clamp(dot(u, c) * 100, 40, 95));
    let idxU = 0;
    let idxC = 0;
    u.forEach((v, i) => {
      if (v > u[idxU]) idxU = i;
    });
    c.forEach((v, i) => {
      if (v > c[idxC]) idxC = i;
    });
    const workStyleNote =
      idxU === idxC
        ? `Both lean ${labels[idxU]} — day-to-day decisions may feel familiar.`
        : `You skew more ${labels[idxU]} while this path emphasizes ${labels[idxC]} work — worth sampling real projects in each style.`;
    const paceSignal = u[4] + u[3] * 0.35 - u[1] * 0.25;
    const deepSignal = u[1] + u[0] * 0.35 - u[4] * 0.2;
    let lifestyleNote = "Balanced between focused stretches and collaborative touchpoints.";
    if (paceSignal > deepSignal + 0.08) {
      lifestyleNote = "Likely more varied pacing and context switching than deep solo focus blocks.";
    } else if (deepSignal > paceSignal + 0.08) {
      lifestyleNote = "Likely more sustained focus blocks and fewer rapid context shifts.";
    }
    return { label, alignment, strength_overlap: overlap, work_style_note: workStyleNote, lifestyle_note: lifestyleNote };
  });
}

export function sliderHash(sliders) {
  const s = sliders || {};
  return `${s.structure ?? 50}-${s.analytical ?? 50}-${s.collaborative ?? 50}-${s.pace ?? 50}`;
}
