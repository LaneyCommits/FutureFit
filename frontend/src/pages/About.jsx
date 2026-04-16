import { Link } from "react-router-dom";

export default function About() {
  return (
    <section className="seo-page">
      <h1>What is ExploringU?</h1>
      <p>
        ExploringU is a career quiz for students who want clearer direction before choosing
        a college major or early career track. The platform maps strengths and tendencies to
        practical pathways you can act on.
      </p>

      <h2>How it works</h2>
      <ol>
        <li>Take a short career path assessment.</li>
        <li>Review your personalized thinking profile.</li>
        <li>Explore major and career recommendations with next steps.</li>
      </ol>

      <p>
        Start with the <Link to="/quiz">career quiz</Link> or browse{" "}
        <Link to="/careers">career directions</Link>.
      </p>
    </section>
  );
}
