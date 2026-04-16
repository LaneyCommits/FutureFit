import { Link } from "react-router-dom";

const PATHWAYS = [
  {
    title: "Analytical Pathways",
    copy: "Great for students who enjoy problem-solving, data, and evidence-based decisions.",
  },
  {
    title: "Creative Pathways",
    copy: "Designed for students who enjoy building ideas, communication, design, and innovation.",
  },
  {
    title: "People and Leadership Pathways",
    copy: "Strong fit for students motivated by collaboration, mentorship, and impact-driven work.",
  },
];

export default function Careers() {
  return (
    <section className="seo-page">
      <h1>Career Quiz for Students: Explore Career Paths</h1>
      <p>
        If you are asking "what career fits me?", this page helps you understand major career
        directions before you take the full assessment.
      </p>

      <div className="seo-grid">
        {PATHWAYS.map((item) => (
          <article key={item.title} className="seo-card">
            <h2>{item.title}</h2>
            <p>{item.copy}</p>
          </article>
        ))}
      </div>

      <p>
        Ready for personalized results? Take the <Link to="/quiz">college major quiz</Link> now.
      </p>
    </section>
  );
}
