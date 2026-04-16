import { Link, useNavigate } from "react-router-dom";
import useMediaQuery from "../hooks/useMediaQuery";
import Logo from "../components/brand/Logo";
import InsightCarousel from "../components/ui/InsightCarousel";

export default function Landing({ user }) {
  const navigate = useNavigate();
  const isDesktop = useMediaQuery("(min-width: 900px)");

  if (isDesktop) {
    return (
      <div className="landing-desktop-layout">
        {!user && (
          <button
            type="button"
            className="landing-return-link"
            onClick={() => navigate("/login")}
          >
            Return to my profile
          </button>
        )}
        <div className="ld-split">
          <div className="ld-split-left">
            <div className="ld-split-content">
              <Logo layout="horizontal" wordmarkSize="md" />
              <h1 className="ld-split-title">
                Find Career Paths That Match Your Strengths
              </h1>
              <p className="ld-split-sub">
                A structured 5-minute career quiz for students that maps your thinking
                patterns to real academic majors and career paths.
              </p>
              <button
                type="button"
                className="btn btn-primary btn-lg ld-split-cta"
                onClick={() => navigate("/quiz")}
              >
                Start Assessment
              </button>
              <div className="landing-meta">
                <span className="landing-meta-item">5 minutes</span>
                <span className="landing-meta-item">Evidence-based</span>
                <span className="landing-meta-item">No signup required</span>
              </div>
            </div>
          </div>
          <div className="ld-split-right">
            <div className="ld-visual">
              <img
                src="/hero-owl.png"
                alt="Calm white owl portrait"
                className="ld-owl-image"
              />
            </div>
          </div>
        </div>
        <section className="landing-seo-sections">
          <article>
            <h2>Career Quiz for Students</h2>
            <p>
              ExploringU gives students a fast, personalized career path assessment that helps
              answer "what career fits me?" without guessing.
            </p>
          </article>
          <article>
            <h2>What is ExploringU?</h2>
            <p>
              ExploringU connects strengths, tendencies, and decision style to practical major
              and career options you can explore with confidence.
            </p>
          </article>
          <article>
            <h2>How it works</h2>
            <p>
              Start the quiz, review your profile, then explore recommendations and next-step
              actions. Learn more on the <Link to="/about">about page</Link>.
            </p>
          </article>
        </section>
        <InsightCarousel />
      </div>
    );
  }

  return (
    <div className="landing-mobile-layout">
      <div className="landing-screen">
        {!user && (
          <button
            type="button"
            className="landing-return-link"
            onClick={() => navigate("/login")}
          >
            Return to my profile
          </button>
        )}
        <div className="landing-content">
          <Logo layout="stacked" wordmarkSize="lg" />
          <h1 className="landing-title">
            Find Career Paths That Match Your Strengths
          </h1>
          <p className="landing-subtitle">
            A structured 5-minute career quiz for students that maps your thinking
            patterns to real academic majors and career paths.
          </p>
          <div className="landing-cta">
            <button
              type="button"
              className="btn btn-primary btn-xl"
              onClick={() => navigate("/quiz")}
            >
              Start Assessment
            </button>
          </div>
          <div className="landing-meta">
            <span className="landing-meta-item">5 minutes</span>
            <span className="landing-meta-item">Evidence-based</span>
            <span className="landing-meta-item">No signup required</span>
          </div>
        </div>
      </div>
      <section className="landing-seo-sections">
        <article>
          <h2>Career Quiz for Students</h2>
          <p>
            ExploringU helps students discover career directions and college majors that align
            with how they naturally think and work.
          </p>
        </article>
        <article>
          <h2>What is ExploringU?</h2>
          <p>
            It is a strengths-based assessment designed to make early career and major decisions
            feel clear, practical, and personalized.
          </p>
        </article>
        <article>
          <h2>How it works</h2>
          <p>
            Take the quiz, review your report, and move into action with next-step guidance. You can
            also explore <Link to="/careers">career pathways</Link>.
          </p>
        </article>
      </section>
      <InsightCarousel />
    </div>
  );
}
