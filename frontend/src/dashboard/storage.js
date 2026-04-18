const SLIDERS_KEY = "exploringu_profile_sliders_v1";
const SAVED_KEY = "exploringu_saved_interests_v1";
const ACTIVITY_KEY = "exploringu_dash_activity_v1";

const defaultSliders = () => ({
  structure: 50,
  analytical: 50,
  collaborative: 50,
  pace: 50,
});

export function loadSliders() {
  try {
    const raw = localStorage.getItem(SLIDERS_KEY);
    if (!raw) return defaultSliders();
    const o = JSON.parse(raw);
    return { ...defaultSliders(), ...o };
  } catch {
    return defaultSliders();
  }
}

export function saveSliders(sliders) {
  localStorage.setItem(SLIDERS_KEY, JSON.stringify(sliders));
}

export function loadSavedInterests() {
  try {
    const raw = localStorage.getItem(SAVED_KEY);
    const arr = JSON.parse(raw || "[]");
    return Array.isArray(arr) ? arr.filter((x) => typeof x === "string" && x.trim()) : [];
  } catch {
    return [];
  }
}

export function saveSavedInterests(list) {
  localStorage.setItem(SAVED_KEY, JSON.stringify(list.slice(0, 40)));
}

export function toggleSavedInterest(name) {
  const t = String(name || "").trim();
  if (!t) return loadSavedInterests();
  const cur = loadSavedInterests();
  const next = cur.includes(t) ? cur.filter((x) => x !== t) : [...cur, t];
  saveSavedInterests(next);
  return next;
}

export function logActivity(type, name, kind = "career") {
  const n = String(name || "").trim();
  if (!n) return;
  try {
    const raw = localStorage.getItem(ACTIVITY_KEY);
    const arr = Array.isArray(JSON.parse(raw || "[]")) ? JSON.parse(raw || "[]") : [];
    arr.push({ ts: Date.now(), type, name: n, kind });
    localStorage.setItem(ACTIVITY_KEY, JSON.stringify(arr.slice(-200)));
  } catch {
    /* ignore */
  }
}

export function loadWeekActivities() {
  const weekMs = 7 * 24 * 60 * 60 * 1000;
  const cutoff = Date.now() - weekMs;
  try {
    const raw = localStorage.getItem(ACTIVITY_KEY);
    const arr = Array.isArray(JSON.parse(raw || "[]")) ? JSON.parse(raw || "[]") : [];
    return arr.filter((x) => x && typeof x.ts === "number" && x.ts >= cutoff);
  } catch {
    return [];
  }
}
