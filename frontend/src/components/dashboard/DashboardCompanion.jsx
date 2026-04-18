import { useCallback, useEffect, useMemo, useState } from "react";
import { getCareerJobs, postInsight } from "../../api/client";
import { alignmentScore0to100, comparePathwayRows, sliderHash } from "../../dashboard/personalize";
import {
  loadSavedInterests,
  loadSliders,
  loadWeekActivities,
  logActivity,
  saveSliders,
  saveSavedInterests,
  toggleSavedInterest,
} from "../../dashboard/storage";

function strHash(s) {
  let h = 2166136261;
  for (let i = 0; i < s.length; i += 1) {
    h ^= s.charCodeAt(i);
    h = Math.imul(h, 16777619);
  }
  return h >>> 0;
}

function rotationKey(userId, sliders) {
  const d = new Date();
  const day = `${d.getUTCFullYear()}-${d.getUTCMonth() + 1}-${d.getUTCDate()}`;
  return `${userId}|${day}|${sliderHash(sliders)}`;
}

export default function DashboardCompanion({ latest, userId, majorNames = [], careerNames = [] }) {
  const [sliders, setSliders] = useState(loadSliders);
  const [saved, setSaved] = useState(loadSavedInterests);
  const [todayText, setTodayText] = useState("");
  const [todayLoading, setTodayLoading] = useState(true);
  const [weeklyText, setWeeklyText] = useState("");
  const [weeklyLoading, setWeeklyLoading] = useState(true);
  const [savedSummary, setSavedSummary] = useState({ summary: "", insight: "" });
  const [savedAiLoading, setSavedAiLoading] = useState(false);

  const [matchQuery, setMatchQuery] = useState("");
  const [matchKind, setMatchKind] = useState("career");
  const [matchResult, setMatchResult] = useState(null);
  const [matchLoading, setMatchLoading] = useState(false);

  const [comparePick, setComparePick] = useState([]);
  const [compareRows, setCompareRows] = useState(null);
  const [compareNarrative, setCompareNarrative] = useState("");
  const [compareLoading, setCompareLoading] = useState(false);

  const [feedCards, setFeedCards] = useState([]);
  const [feedLoading, setFeedLoading] = useState(true);

  const profile = useMemo(
    () => ({
      primary_key: latest?.primary_key,
      primary_name: latest?.primary_name,
      secondary_key: latest?.secondary_key,
      secondary_name: latest?.secondary_name,
      scores: latest?.scores || {},
    }),
    [latest],
  );

  const suggestions = useMemo(() => {
    const m = majorNames.map((x) => String(x).trim()).filter(Boolean);
    const c = careerNames.map((x) => String(x).trim()).filter(Boolean);
    return [...new Set([...m, ...c])].slice(0, 24);
  }, [majorNames, careerNames]);

  const fetchToday = useCallback(async () => {
    setTodayLoading(true);
    try {
      const res = await postInsight("today", {
        profile,
        sliders,
        rotation_key: rotationKey(userId, sliders),
      });
      setTodayText(res.text || "");
    } catch {
      setTodayText(
        "Adjust the sliders below to see how your exploration lens shifts — small tweaks can surface different pathways.",
      );
    } finally {
      setTodayLoading(false);
    }
  }, [profile, sliders, userId]);

  useEffect(() => {
    saveSliders(sliders);
  }, [sliders]);

  useEffect(() => {
    const t = setTimeout(() => fetchToday(), 320);
    return () => clearTimeout(t);
  }, [fetchToday]);

  useEffect(() => {
    let cancel = false;
    async function week() {
      setWeeklyLoading(true);
      const acts = loadWeekActivities().map((a) => ({ name: a.name, kind: a.kind || "career" }));
      try {
        const res = await postInsight("weekly-reflection", { profile, activities: acts });
        if (!cancel) setWeeklyText(res.text || "");
      } catch {
        if (!cancel) setWeeklyText("");
      } finally {
        if (!cancel) setWeeklyLoading(false);
      }
    }
    week();
    return () => {
      cancel = true;
    };
  }, [profile, latest?.id]);

  const refreshSavedAi = useCallback(async () => {
    if (!saved.length) {
      setSavedSummary({ summary: "", insight: "" });
      return;
    }
    setSavedAiLoading(true);
    try {
      const res = await postInsight("saved-pattern", { profile, saved });
      setSavedSummary({
        summary: res.summary || "",
        insight: res.insight || "",
      });
    } catch {
      setSavedSummary({ summary: "", insight: "" });
    } finally {
      setSavedAiLoading(false);
    }
  }, [profile, saved]);

  useEffect(() => {
    refreshSavedAi();
  }, [refreshSavedAi]);

  useEffect(() => {
    let cancel = false;
    async function loadFeed() {
      setFeedLoading(true);
      try {
        const jobs = await getCareerJobs(60);
        const titles = (Array.isArray(jobs) ? jobs : [])
          .map((j) => j.title)
          .filter(Boolean);
        const pool = titles.length ? titles : suggestions;
        const seed = Number(userId) || 1;
        const rotated = [...pool].sort((a, b) => (strHash(a + seed) % 7) - (strHash(b + seed) % 7));
        const pick = rotated.slice(0, 8);
        if (!pick.length) {
          if (!cancel) setFeedCards([]);
          return;
        }
        const res = await postInsight("career-feed", { profile, sliders, careers: pick });
        if (!cancel) setFeedCards(Array.isArray(res.cards) ? res.cards : []);
      } catch {
        if (!cancel) setFeedCards([]);
      } finally {
        if (!cancel) setFeedLoading(false);
      }
    }
    loadFeed();
    return () => {
      cancel = true;
    };
  }, [profile, sliders, userId, suggestions, latest?.id]);

  function setSlider(key, value) {
    setSliders((prev) => ({ ...prev, [key]: value }));
  }

  async function runMatch() {
    const target = matchQuery.trim();
    if (!target) return;
    logActivity("match", target, matchKind);
    setMatchLoading(true);
    const localScore = alignmentScore0to100(latest?.scores || {}, sliders, target);
    setMatchResult({
      score: localScore,
      why_fit: "",
      challenges: "",
      alternatives: [],
      pending: true,
    });
    try {
      const res = await postInsight("career-match", {
        profile,
        sliders,
        target,
        kind: matchKind,
      });
      setMatchResult({
        score: res.score ?? localScore,
        why_fit: res.why_fit || "",
        challenges: res.challenges || "",
        alternatives: res.alternatives || [],
        pending: false,
      });
    } catch {
      setMatchResult({
        score: localScore,
        why_fit:
          "We could not reach the insight service. Your local fit estimate is still available — try again in a moment.",
        challenges: "Check your connection or API configuration.",
        alternatives: [],
        pending: false,
      });
    } finally {
      setMatchLoading(false);
    }
  }

  async function runCompare() {
    if (comparePick.length < 2) return;
    comparePick.forEach((name) => logActivity("compare", name, "pathway"));
    setCompareLoading(true);
    const localRows = comparePathwayRows(latest?.scores || {}, sliders, comparePick);
    setCompareRows(localRows);
    setCompareNarrative("");
    try {
      const res = await postInsight("compare", { profile, sliders, items: comparePick });
      if (Array.isArray(res.rows) && res.rows.length) {
        setCompareRows(res.rows);
        setCompareNarrative(res.narrative || "");
      }
    } catch {
      /* keep local rows */
    } finally {
      setCompareLoading(false);
    }
  }

  function toggleCompareChip(label) {
    const t = String(label).trim();
    if (!t) return;
    setComparePick((prev) => {
      if (prev.includes(t)) return prev.filter((x) => x !== t);
      if (prev.length >= 3) return [...prev.slice(1), t];
      return [...prev, t];
    });
  }

  function onSaveToggle(name) {
    const next = toggleSavedInterest(name);
    setSaved(next);
    logActivity("save", name, "saved");
  }

  return (
    <div className="dash-companion">
      <section className="dashboard-soft-card dash-insight-card">
        <div className="dash-insight-head">
          <div>
            <p className="dashboard-kicker">Today&apos;s insight</p>
            <h2 className="dash-card-title">Personalized for you</h2>
          </div>
          <button type="button" className="dash-ghost-btn" onClick={() => fetchToday()} disabled={todayLoading}>
            Refresh
          </button>
        </div>
        {todayLoading ? (
          <p className="dashboard-muted-copy">Generating…</p>
        ) : (
          <p className="dash-insight-body">{todayText}</p>
        )}
      </section>

      <div className="dash-companion-grid">
        <section className="dashboard-soft-card dash-weekly-card">
          <p className="dashboard-kicker">This week</p>
          <h2 className="dash-card-title">Reflection</h2>
          {weeklyLoading ? (
            <p className="dashboard-muted-copy">Summarizing…</p>
          ) : (
            <p className="dash-weekly-body">{weeklyText}</p>
          )}
        </section>

        <section className="dashboard-soft-card dash-sliders-card">
          <p className="dashboard-kicker">Your lens</p>
          <h2 className="dash-card-title">Profile adjustment</h2>
          <p className="dashboard-muted-copy dash-tight-top">
            Tune these to reflect how you like to work — scores and feed update automatically.
          </p>
          <div className="dash-slider-list">
            {[
              { key: "structure", left: "Flexibility", right: "Structure" },
              { key: "analytical", left: "Creative", right: "Analytical" },
              { key: "collaborative", left: "Independent", right: "Collaborative" },
              { key: "pace", left: "Deep focus", right: "Fast-paced" },
            ].map((row) => (
              <label key={row.key} className="dash-slider-row">
                <div className="dash-slider-labels">
                  <span>{row.left}</span>
                  <span>{row.right}</span>
                </div>
                <input
                  type="range"
                  min={0}
                  max={100}
                  value={sliders[row.key] ?? 50}
                  onChange={(e) => setSlider(row.key, Number(e.target.value))}
                />
              </label>
            ))}
          </div>
        </section>
      </div>

      <section className="dashboard-soft-card dash-saved-card">
        <div className="dash-insight-head">
          <div>
            <p className="dashboard-kicker">Saved interests</p>
            <h2 className="dash-card-title">Pattern snapshot</h2>
          </div>
        </div>
        {!saved.length ? (
          <p className="dashboard-muted-copy">Save items from the feed or match results to see themes here.</p>
        ) : (
          <>
            <div className="dash-chip-row">
              {saved.map((s) => (
                <button
                  key={s}
                  type="button"
                  className="dash-saved-chip"
                  onClick={() => {
                    const next = saved.filter((x) => x !== s);
                    saveSavedInterests(next);
                    setSaved(next);
                  }}
                >
                  {s} ×
                </button>
              ))}
            </div>
            {savedAiLoading ? (
              <p className="dashboard-muted-copy dash-tight-top">Reading your pattern…</p>
            ) : (
              <>
                {savedSummary.summary && <p className="dash-saved-summary">{savedSummary.summary}</p>}
                {savedSummary.insight && <p className="dash-saved-insight">{savedSummary.insight}</p>}
              </>
            )}
          </>
        )}
      </section>

      <section className="dashboard-soft-card dash-match-card">
        <p className="dashboard-kicker">Career match explorer</p>
        <h2 className="dash-card-title">Search a pathway</h2>
        <div className="dash-match-toolbar">
          <input
            className="dash-text-input"
            list="dash-match-suggestions"
            placeholder="e.g. UX Design, Psychology, Data Analyst…"
            value={matchQuery}
            onChange={(e) => setMatchQuery(e.target.value)}
          />
          <datalist id="dash-match-suggestions">
            {suggestions.map((s) => (
              <option key={s} value={s} />
            ))}
          </datalist>
          <div className="dash-toggle-row">
            <button
              type="button"
              className={`dashboard-toggle ${matchKind === "career" ? "is-active" : ""}`}
              onClick={() => setMatchKind("career")}
            >
              Career
            </button>
            <button
              type="button"
              className={`dashboard-toggle ${matchKind === "major" ? "is-active" : ""}`}
              onClick={() => setMatchKind("major")}
            >
              Major
            </button>
          </div>
          <button type="button" className="btn btn-primary dash-match-btn" onClick={runMatch} disabled={matchLoading}>
            {matchLoading ? "Analyzing…" : "Get match"}
          </button>
        </div>
        {matchResult && (
          <div className="dash-match-result">
            <div className="dash-match-score">
              <span className="dashboard-score-kicker">Alignment</span>
              <strong>{matchResult.score}%</strong>
            </div>
            {matchResult.pending ? (
              <p className="dashboard-muted-copy dash-tight-top">Personalizing explanation…</p>
            ) : (
              <>
                <p className="dash-match-why">{matchResult.why_fit}</p>
                <p className="dash-match-challenge">
                  <span className="dash-label">Consider</span> {matchResult.challenges}
                </p>
                {!!matchResult.alternatives?.length && (
                  <div className="dash-alt-row">
                    <span className="dash-label">Alternatives</span>
                    <div className="dash-chip-row">
                      {matchResult.alternatives.map((a) => (
                        <button key={a} type="button" className="dash-target-chip" onClick={() => setMatchQuery(a)}>
                          {a}
                        </button>
                      ))}
                    </div>
                  </div>
                )}
              </>
            )}
            {matchQuery.trim() && (
              <button type="button" className="dash-ghost-btn dash-save-inline" onClick={() => onSaveToggle(matchQuery.trim())}>
                {saved.includes(matchQuery.trim()) ? "Remove from saved" : "Save to interests"}
              </button>
            )}
          </div>
        )}
      </section>

      <section className="dashboard-soft-card dash-compare-card">
        <p className="dashboard-kicker">Compare mode</p>
        <h2 className="dash-card-title">Two or three pathways</h2>
        <p className="dashboard-muted-copy dash-tight-top">Select up to three, then generate a side-by-side readout.</p>
        <div className="dash-target-grid">
          {suggestions.map((target) => (
            <button
              key={target}
              type="button"
              className={`dashboard-target-chip ${comparePick.includes(target) ? "is-active" : ""}`}
              onClick={() => toggleCompareChip(target)}
            >
              {target}
            </button>
          ))}
        </div>
        <button
          type="button"
          className="btn btn-primary dash-compare-run"
          onClick={runCompare}
          disabled={comparePick.length < 2 || compareLoading}
        >
          {compareLoading ? "Comparing…" : "Compare selected"}
        </button>
        {compareRows && compareRows.length > 0 && (
          <div className="dash-compare-results">
            {compareNarrative && <p className="dash-compare-narrative">{compareNarrative}</p>}
            <div className="dash-compare-columns">
              {compareRows.map((row) => (
                <article key={row.label} className="dash-compare-column">
                  <h3>{row.label}</h3>
                  <p className="dash-compare-metric">
                    <span>Alignment</span> <strong>{row.alignment}%</strong>
                  </p>
                  <p className="dash-compare-metric">
                    <span>Strength overlap</span>{" "}
                    <strong>{row.strength_overlap ?? row.strengthOverlap ?? "—"}%</strong>
                  </p>
                  <p className="dash-compare-note">{row.work_style_note || row.workStyleNote}</p>
                  <p className="dash-compare-note">{row.lifestyle_note || row.lifestyleNote}</p>
                </article>
              ))}
            </div>
          </div>
        )}
      </section>

      <section className="dashboard-soft-card dash-feed-card">
        <div className="dash-insight-head">
          <div>
            <p className="dashboard-kicker">Career feed</p>
            <h2 className="dash-card-title">Tailored exploration cards</h2>
          </div>
        </div>
        {feedLoading ? (
          <p className="dashboard-muted-copy">Building your feed…</p>
        ) : feedCards.length === 0 ? (
          <p className="dashboard-muted-copy">No feed items yet. Try refreshing after the careers catalog loads.</p>
        ) : (
          <div className="dash-feed-scroll">
            {feedCards.map((card) => (
              <article key={card.name} className="dash-feed-card-item">
                <h3>{card.name}</h3>
                <p className="dash-feed-desc">{card.short_description || card.shortDescription}</p>
                <p className="dash-feed-why">{card.why_fit || card.whyFit}</p>
                <div className="dash-feed-actions">
                  <button type="button" className="btn btn-primary" onClick={() => onSaveToggle(card.name)}>
                    {saved.includes(card.name) ? "Saved" : "Save"}
                  </button>
                  <button
                    type="button"
                    className="dash-ghost-btn"
                    onClick={() => {
                      setMatchQuery(card.name);
                      logActivity("explore", card.name, "career");
                    }}
                  >
                    Explore
                  </button>
                </div>
              </article>
            ))}
          </div>
        )}
      </section>
    </div>
  );
}
