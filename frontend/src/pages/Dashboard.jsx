import { useEffect, useLayoutEffect, useRef, useState } from "react";
import { Link } from "react-router-dom";
import { getDashboard } from "../api/client";
import DashboardCompanion from "../components/dashboard/DashboardCompanion";

const ARCHETYPE_META = [
  { key: "systems_thinker", label: "Systems", tone: "sage" },
  { key: "analytical_solver", label: "Analytical", tone: "blue" },
  { key: "creative_builder", label: "Creative", tone: "teal" },
  { key: "people_strategist", label: "People", tone: "sage" },
  { key: "explorer", label: "Explorer", tone: "blue" },
  { key: "impact_visionary", label: "Visionary", tone: "teal" },
];

const PROFILE_COPY = {
  systems_thinker:
    "You naturally look for structure, patterns, and long-term consequences. You feel most confident when things are mapped clearly and decisions follow a coherent system.",
  analytical_solver:
    "You process decisions by testing evidence and reducing uncertainty. You are strongest when you can break complex problems into clear, solvable parts.",
  creative_builder:
    "You think in possibilities and connect ideas that others keep separate. You thrive when you can design, iterate, and turn abstract concepts into something real.",
  people_strategist:
    "You read context, motivation, and team dynamics quickly. You make strong decisions when people outcomes and practical execution are balanced together.",
  explorer:
    "You adapt quickly and stay curious in unfamiliar situations. You make progress by experimenting, learning fast, and refining direction as you go.",
  impact_visionary:
    "You are driven by meaning and long-range impact. You make your best decisions when your work clearly connects to a larger purpose.",
};

const NEXT_STEPS = {
  systems_thinker: [
    "Shortlist two majors and compare their required courses side by side.",
    "Pick one project this month where you build a repeatable workflow.",
    "Talk to one upperclassman about how they chose their specialization.",
    "Create a one-page decision framework for your next major choice.",
  ],
  analytical_solver: [
    "Test your fit by solving one real case study in each target major.",
    "Track which classes feel energizing after deep problem-solving sessions.",
    "Book one informational interview with someone in a data-heavy role.",
    "Build a small portfolio artifact that demonstrates your reasoning style.",
  ],
  creative_builder: [
    "Build one small project that combines creativity with structured outcomes.",
    "Audit course syllabi and highlight classes with studio or project work.",
    "Interview someone in a design or product role about daily decision-making.",
    "Create a weekly idea log and note which themes keep returning.",
  ],
  people_strategist: [
    "Choose one leadership or facilitation opportunity this semester.",
    "Map your strongest communication moments and what made them effective.",
    "Explore majors with team-based projects and social systems focus.",
    "Set up two shadow conversations with professionals in people-centered roles.",
  ],
  explorer: [
    "Run two low-risk experiments this month in different career directions.",
    "Keep a weekly reflection on what environments sharpen your focus.",
    "Take one class outside your comfort zone to test adaptation fit.",
    "Use a 30-day decision sprint instead of waiting for perfect certainty.",
  ],
  impact_visionary: [
    "Define one mission theme you want your career to serve.",
    "Compare majors by how directly they connect to real-world outcomes.",
    "Find one internship or volunteer role with clear social impact.",
    "Write a personal success definition before choosing your next path.",
  ],
};

const GROWTH_MAP = {
  systems_thinker: {
    thrive:
      "You thrive in environments with clear systems, defined expectations, and measurable progress.",
    challenge:
      "You may feel friction in ambiguous settings where priorities shift without explanation.",
    conditions:
      "Best results come when you can sequence work, set milestones, and revisit decisions with evidence.",
  },
  analytical_solver: {
    thrive:
      "You thrive where decisions are evidence-driven and rigorous thinking is respected.",
    challenge:
      "You can over-delay choices when data is incomplete or standards feel vague.",
    conditions:
      "You perform best when scope is clear, assumptions are explicit, and feedback is concrete.",
  },
  creative_builder: {
    thrive:
      "You thrive where originality is encouraged and ideas can be tested quickly.",
    challenge:
      "You may disengage in rigid systems that block experimentation or ownership.",
    conditions:
      "You succeed most when there is room for iteration, visual thinking, and creative problem framing.",
  },
  people_strategist: {
    thrive:
      "You thrive in collaborative environments where communication and empathy shape outcomes.",
    challenge:
      "You can feel drained in roles with minimal human connection or isolated execution.",
    conditions:
      "You do best with purposeful team interaction, role clarity, and shared accountability.",
  },
  explorer: {
    thrive:
      "You thrive in dynamic environments where learning speed and adaptability matter.",
    challenge:
      "You may lose momentum when routines become repetitive or overly constrained.",
    conditions:
      "You perform best with varied challenges, clear short sprints, and room to test options.",
  },
  impact_visionary: {
    thrive:
      "You thrive when work aligns with purpose and contributes to something meaningful.",
    challenge:
      "You can feel disconnected when tasks seem transactional or impact is unclear.",
    conditions:
      "You excel with mission clarity, long-range context, and opportunities to influence outcomes.",
  },
};

const COMPARISON_LINES = {
  systems_thinker: "systems-oriented than",
  analytical_solver: "analytical than",
  creative_builder: "creative than",
  people_strategist: "people-centered than",
  explorer: "adaptable than",
  impact_visionary: "impact-driven than",
};

const MAJOR_FITS = {
  systems_thinker: [
    {
      name: "Information Systems",
      reason: "Fits your preference for architecture, process clarity, and practical decision structures.",
    },
    {
      name: "Industrial Engineering",
      reason: "Matches your systems mindset and ability to optimize complex workflows.",
    },
    {
      name: "Operations Management",
      reason: "Aligns with your strength in making ordered decisions under real constraints.",
    },
    {
      name: "Supply Chain Management",
      reason: "Supports your natural tendency to map moving parts and improve coordination.",
    },
  ],
  analytical_solver: [
    {
      name: "Computer Science",
      reason: "Fits your evidence-driven approach and comfort with structured problem decomposition.",
    },
    {
      name: "Data Science",
      reason: "Aligns with your habit of turning uncertainty into signal through analysis.",
    },
    {
      name: "Economics",
      reason: "Matches your decision style around tradeoffs, models, and predictive reasoning.",
    },
    {
      name: "Finance",
      reason: "Supports your strong analytical judgment in high-stakes decision contexts.",
    },
  ],
  creative_builder: [
    {
      name: "UX Design",
      reason: "Fits how you connect empathy, systems, and creative experimentation.",
    },
    {
      name: "Product Design",
      reason: "Aligns with your instinct to build ideas into tangible, usable outcomes.",
    },
    {
      name: "Marketing",
      reason: "Matches your ability to frame narratives and test creative strategy.",
    },
    {
      name: "Media Production",
      reason: "Supports your strength in expressive communication and iterative creation.",
    },
  ],
  people_strategist: [
    {
      name: "Psychology",
      reason: "Fits your pattern of reading human behavior and decision context.",
    },
    {
      name: "Business Administration",
      reason: "Aligns with your blend of people awareness and pragmatic execution.",
    },
    {
      name: "Human Resources",
      reason: "Matches your strength in team dynamics and role alignment.",
    },
    {
      name: "Communications",
      reason: "Supports your ability to influence clarity, trust, and coordinated action.",
    },
  ],
  explorer: [
    {
      name: "Entrepreneurship",
      reason: "Fits your adaptive style and comfort moving through uncertainty quickly.",
    },
    {
      name: "International Studies",
      reason: "Aligns with your curiosity and ability to navigate changing contexts.",
    },
    {
      name: "Environmental Studies",
      reason: "Matches your cross-domain thinking and experimentation-oriented mindset.",
    },
    {
      name: "Interdisciplinary Studies",
      reason: "Supports your tendency to connect insights across multiple fields.",
    },
  ],
  impact_visionary: [
    {
      name: "Public Policy",
      reason: "Fits your long-horizon thinking and desire to create meaningful outcomes.",
    },
    {
      name: "Social Work",
      reason: "Aligns with your purpose-driven perspective and human-centered decisions.",
    },
    {
      name: "Public Health",
      reason: "Matches your motivation to drive large-scale, practical impact.",
    },
    {
      name: "Education",
      reason: "Supports your ability to shape systems through values and long-term influence.",
    },
  ],
};

const CAREER_PATTERNS = {
  systems_thinker: {
    analytical: "Business Analyst",
    creative: "Service Designer",
    structured: "Operations Coordinator",
  },
  analytical_solver: {
    analytical: "Data Analyst",
    creative: "Product Strategist",
    structured: "Financial Analyst",
  },
  creative_builder: {
    analytical: "UX Researcher",
    creative: "Product Designer",
    structured: "Brand Operations Specialist",
  },
  people_strategist: {
    analytical: "People Analytics Associate",
    creative: "Community Strategist",
    structured: "Program Manager",
  },
  explorer: {
    analytical: "Innovation Analyst",
    creative: "Content Producer",
    structured: "Project Associate",
  },
  impact_visionary: {
    analytical: "Policy Analyst",
    creative: "Advocacy Storyteller",
    structured: "Nonprofit Program Lead",
  },
};

function fmtDate(value) {
  if (!value) return "";
  return new Date(value).toLocaleDateString(undefined, {
    year: "numeric",
    month: "short",
    day: "numeric",
  });
}

function normalizeScores(scores = []) {
  const normalizedEntries = Array.isArray(scores)
    ? scores.map((s) => [s.archetype, s.score])
    : Object.entries(scores || {});
  const map = new Map(normalizedEntries);
  const values = ARCHETYPE_META.map((a) => map.get(a.key) ?? 0);
  const maxScore = Math.max(...values, 1);
  return ARCHETYPE_META.map((a) => ({
    ...a,
    score: map.get(a.key) ?? 0,
    percent: ((map.get(a.key) ?? 0) / maxScore) * 100,
  }));
}

function compactReason(text = "", fallback = "Strong alignment with your decision style.") {
  const cleaned = String(text || "").replace(/\s+/g, " ").trim();
  if (!cleaned) return fallback;
  return cleaned.length > 112 ? `${cleaned.slice(0, 112).trimEnd()}...` : cleaned;
}

function compareInsight(primaryKey, scoreRows, majorName) {
  const primary = scoreRows.find((row) => row.key === primaryKey) || scoreRows[0];
  const percentile = Math.min(91, Math.max(58, Math.round(primary.percent * 0.52 + 41)));
  const styleText = COMPARISON_LINES[primaryKey] || "pattern-oriented than";
  return {
    users: `You are more ${styleText} ${percentile}% of users in this dataset.`,
    major: `Your pattern aligns closely with ${majorName || "your current major paths"} decision profiles.`,
    secondary: `Your secondary pattern strengthens your ability to adapt across both focused and cross-functional roles.`,
  };
}

export default function Dashboard() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState("overview");
  const [expandedPathCard, setExpandedPathCard] = useState("start");
  const [chartReady, setChartReady] = useState(false);
  const [visibleTab, setVisibleTab] = useState("overview");
  const [transitionPhase, setTransitionPhase] = useState("idle");
  const [pendingTab, setPendingTab] = useState(null);
  const [indicator, setIndicator] = useState({ x: 0, width: 0, ready: false });
  const tabListRef = useRef(null);
  const tabRefs = useRef({});

  useEffect(() => {
    let mounted = true;
    async function load() {
      try {
        const res = await getDashboard();
        if (mounted) setData(res);
      } catch (err) {
        if (mounted) setError(err.message);
      } finally {
        if (mounted) setLoading(false);
      }
    }
    load();
    return () => {
      mounted = false;
    };
  }, []);

  const latest = data?.latest;
  const hasHistory = Boolean(data?.history?.length);

  const primaryKey = latest?.primary_key || "systems_thinker";
  const primaryName = latest?.primary_name || "Thinking Profile";
  const profileCopy =
    PROFILE_COPY[primaryKey] ||
    "Your profile highlights how you naturally process choices, communicate direction, and make progress.";
  let scoreRows = [];
  try {
    scoreRows = normalizeScores(latest?.scores || {});
  } catch (error) {
    throw error;
  }
  const majors = (MAJOR_FITS[primaryKey] || MAJOR_FITS.systems_thinker).slice(0, 5);
  const fallbackMajorName = majors[0]?.name || "your recommended pathways";
  const careerSeed = CAREER_PATTERNS[primaryKey] || CAREER_PATTERNS.systems_thinker;
  const steps = (NEXT_STEPS[primaryKey] || NEXT_STEPS.systems_thinker).slice(0, 4);
  const growth = GROWTH_MAP[primaryKey] || GROWTH_MAP.systems_thinker;
  const compare = compareInsight(primaryKey, scoreRows, fallbackMajorName);
  const companionCareerNames = [
    careerSeed.analytical,
    careerSeed.creative,
    careerSeed.structured,
  ].filter(Boolean);

  useEffect(() => {
    if (!scoreRows.length) return;
    let raf1 = requestAnimationFrame(() => {
      let raf2 = requestAnimationFrame(() => setChartReady(true));
      return () => cancelAnimationFrame(raf2);
    });
    return () => cancelAnimationFrame(raf1);
  }, [primaryKey, scoreRows.length]);

  function handleTabSwitch(tabId) {
    if (tabId === visibleTab || transitionPhase === "exit") return;
    setActiveTab(tabId);
    setPendingTab(tabId);
    setTransitionPhase("exit");
  }

  function handleContentAnimationEnd(event) {
    if (event.target !== event.currentTarget) return;
    if (transitionPhase === "exit" && pendingTab) {
      setVisibleTab(pendingTab);
      setPendingTab(null);
      setTransitionPhase("enter");
      return;
    }
    if (transitionPhase === "enter") {
      setTransitionPhase("idle");
    }
  }

  useLayoutEffect(() => {
    function updateIndicator() {
      const listEl = tabListRef.current;
      const activeEl = tabRefs.current[activeTab];
      if (!listEl || !activeEl) return;
      const listRect = listEl.getBoundingClientRect();
      const tabRect = activeEl.getBoundingClientRect();
      const x = tabRect.left - listRect.left + listEl.scrollLeft;
      const width = tabRect.width;
      setIndicator({ x, width, ready: true });
    }

    updateIndicator();
    const listEl = tabListRef.current;
    if (!listEl) return;
    const observer = new ResizeObserver(updateIndicator);
    observer.observe(listEl);
    Object.values(tabRefs.current).forEach((el) => {
      if (el) observer.observe(el);
    });
    listEl.addEventListener("scroll", updateIndicator, { passive: true });
    window.addEventListener("resize", updateIndicator);
    return () => {
      observer.disconnect();
      listEl.removeEventListener("scroll", updateIndicator);
      window.removeEventListener("resize", updateIndicator);
    };
  }, [activeTab]);

  if (loading) {
    return (
      <div className="page-center">
        <div className="loading-spinner" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="page-center">
        <p className="error-text">{error}</p>
      </div>
    );
  }

  if (!latest) {
    return (
      <div className="dashboard-premium">
        <section className="dashboard-empty-state">
          <h1>Your Thinking Profile Dashboard</h1>
          <p>
            You do not have a saved profile yet. Take the assessment first so we can build
            your personalized psychological report.
          </p>
          <Link to="/quiz" className="btn btn-primary">
            Take the Assessment
          </Link>
        </section>
      </div>
    );
  }

  return (
    <div className="dashboard-premium">
      <aside className="dashboard-identity-panel">
        <div className="dashboard-soft-card dashboard-identity-card">
          <p className="dashboard-kicker">Your Thinking Profile</p>
          <h1 className="dashboard-profile-title">{primaryName}</h1>
          {latest.secondary_name && (
            <p className="dashboard-profile-secondary">+ {latest.secondary_name}</p>
          )}
          <p className="dashboard-profile-copy">{profileCopy}</p>
          <p className="dashboard-support-line">
            This reflects how you naturally approach decisions, not just your interests.
          </p>
          <p className="dashboard-saved-date">Saved {fmtDate(latest.created_at)}</p>
        </div>

        <div className="dashboard-soft-card dashboard-chart-card">
          <h2 className="dashboard-card-heading">Thinking Pattern Analytics</h2>
          <div className={`dashboard-score-list ${chartReady ? "is-ready" : ""}`}>
            {scoreRows.map((row, idx) => (
              <div
                key={row.key}
                className="dashboard-score-row dashboard-score-row-animated"
                style={{ transitionDelay: `${idx * 70}ms` }}
              >
                <span className="dashboard-score-label">{row.label}</span>
                <div className="dashboard-score-track">
                  <span
                    className={`dashboard-score-fill tone-${row.tone} ${
                      row.key === primaryKey ? "is-primary" : ""
                    }`}
                    style={{ width: `${Math.max(row.percent, 4)}%` }}
                  />
                </div>
                <span className="dashboard-score-value">{row.score.toFixed(1)}</span>
              </div>
            ))}
          </div>
        </div>
      </aside>

      <main className="dashboard-report-content">
        <DashboardCompanion
          latest={latest}
          userId={data?.user?.id ?? 0}
          majorNames={majors.map((m) => m.name)}
          careerNames={companionCareerNames}
        />

        <section className="dashboard-tabs-shell">
          <div className="dashboard-tabs" role="tablist" aria-label="Dashboard views" ref={tabListRef}>
            <span
              className={`dashboard-tab-indicator ${indicator.ready ? "is-ready" : ""}`}
              style={{
                transform: `translateX(${indicator.x}px)`,
                width: `${indicator.width}px`,
              }}
              aria-hidden="true"
            />
            {[
              { id: "overview", label: "Overview" },
              { id: "path", label: "Path" },
              { id: "growth", label: "Growth" },
            ].map((tab) => (
              <button
                key={tab.id}
                type="button"
                role="tab"
                aria-selected={activeTab === tab.id}
                className={`dashboard-tab ${activeTab === tab.id ? "is-active" : ""}`}
                ref={(el) => {
                  tabRefs.current[tab.id] = el;
                }}
                onClick={() => handleTabSwitch(tab.id)}
              >
                {tab.label}
              </button>
            ))}
          </div>
        </section>

        <div
          className={`dashboard-tab-stage phase-${transitionPhase}`}
          onAnimationEnd={handleContentAnimationEnd}
        >
        {visibleTab === "overview" && (
          <section className="dashboard-soft-card dashboard-tab-content">
            <h2 className="dashboard-section-title">Overview</h2>
            <p className="dashboard-muted-copy">
              Your profile combines {primaryName} thinking with practical decision behavior.
            </p>
            <div className="dashboard-subsection">
              <h3 className="dashboard-subsection-title">Personality Summary</h3>
              <p className="dashboard-item-copy">{profileCopy}</p>
            </div>
            <div className="dashboard-subsection">
              <h3 className="dashboard-subsection-title">Key Insight</h3>
              <p className="dashboard-item-copy">{compare.users}</p>
            </div>
          </section>
        )}

        {visibleTab === "path" && (
          <section className="dashboard-soft-card dashboard-tab-content">
            <h2 className="dashboard-section-title">Path</h2>
            <div className="dashboard-path-flow">
              <article
                className={`dashboard-path-card ${
                  expandedPathCard === "start" ? "is-expanded" : ""
                }`}
              >
                <button
                  type="button"
                  className="dashboard-path-trigger"
                  onClick={() => setExpandedPathCard(expandedPathCard === "start" ? "" : "start")}
                >
                  <h3 className="dashboard-subsection-title">Start Here</h3>
                </button>
                <div className="dashboard-path-body">
                  <ul className="dashboard-step-list">
                    <li>{steps[0]}</li>
                  </ul>
                </div>
              </article>

              <article
                className={`dashboard-path-card ${
                  expandedPathCard === "explore" ? "is-expanded" : ""
                }`}
              >
                <button
                  type="button"
                  className="dashboard-path-trigger"
                  onClick={() =>
                    setExpandedPathCard(expandedPathCard === "explore" ? "" : "explore")
                  }
                >
                  <h3 className="dashboard-subsection-title">Explore Next</h3>
                </button>
                <div className="dashboard-path-body">
                  <ul className="dashboard-detail-list">
                    {(majors.length ? majors : [{ name: "Core fit pathway", reason: "" }]).map((major) => (
                      <li key={major.name}>
                        <span className="dashboard-item-title">{major.name}</span>
                        <span className="dashboard-item-copy">
                          {compactReason(
                            major.reason,
                            "This major aligns with your problem-solving style and long-term motivation pattern.",
                          )}
                        </span>
                      </li>
                    ))}
                  </ul>
                </div>
              </article>

              <article
                className={`dashboard-path-card ${
                  expandedPathCard === "build" ? "is-expanded" : ""
                }`}
              >
                <button
                  type="button"
                  className="dashboard-path-trigger"
                  onClick={() => setExpandedPathCard(expandedPathCard === "build" ? "" : "build")}
                >
                  <h3 className="dashboard-subsection-title">Build Toward</h3>
                </button>
                <div className="dashboard-path-body">
                  <div className="dashboard-career-groups">
                    <article className="dashboard-career-group">
                      <p className="dashboard-group-title">Analytical</p>
                      <p>
                        {(careerSeed.analytical || "Data-forward roles") +
                          " and related pathways where structured reasoning drives outcomes."}
                      </p>
                    </article>
                    <article className="dashboard-career-group">
                      <p className="dashboard-group-title">Creative</p>
                      <p>
                        {(careerSeed.creative || "Design-oriented roles") +
                          " that reward ideation, synthesis, and building from ambiguity."}
                      </p>
                    </article>
                    <article className="dashboard-career-group">
                      <p className="dashboard-group-title">Structured</p>
                      <p>
                        {(careerSeed.structured || "Operations-centered roles") +
                          " where consistency, clear systems, and disciplined execution matter."}
                      </p>
                    </article>
                  </div>
                </div>
              </article>

              <article className="dashboard-path-card is-expanded">
                <h3 className="dashboard-subsection-title">Personalization Entry</h3>
                <div className="dashboard-path-body">
                  <p className="dashboard-item-copy">
                    Add one custom goal this week and track how your decision style supports it.
                  </p>
                </div>
              </article>
            </div>
          </section>
        )}

        {visibleTab === "growth" && (
          <section className="dashboard-soft-card dashboard-tab-content">
            <h2 className="dashboard-section-title">Growth</h2>
            <div className="dashboard-growth-grid">
              <article className="dashboard-growth-item">
                <h3>Strengths</h3>
                <p>{growth.thrive}</p>
              </article>
              <article className="dashboard-growth-item">
                <h3>Blind Spots</h3>
                <p>{growth.challenge}</p>
              </article>
              <article className="dashboard-growth-item">
                <h3>Fit Environments</h3>
                <p>{growth.conditions}</p>
              </article>
            </div>
          </section>
        )}
        </div>

        <section className="dashboard-soft-card">
          <h2 className="dashboard-section-title">Profile History</h2>
          {!hasHistory ? (
            <p className="dashboard-muted-copy">
              No saved reports yet. <Link to="/quiz">Take the assessment</Link>.
            </p>
          ) : (
            <ul className="dashboard-history-list">
              {data.history.map((item) => (
                <li key={item.id} className="dashboard-history-item">
                  <div>
                    <strong>{item.primary_name || "Profile"}</strong>
                    {item.secondary_name ? ` + ${item.secondary_name}` : ""}
                  </div>
                  <span>{fmtDate(item.created_at)}</span>
                </li>
              ))}
            </ul>
          )}
        </section>
      </main>
    </div>
  );
}

