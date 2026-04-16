import { useEffect, useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { login } from "../api/client";

export default function Login({ onAuth, user }) {
  const location = useLocation();
  const navigate = useNavigate();
  const pendingQuiz = location.state?.pendingQuiz || null;
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (user) navigate("/dashboard");
  }, [user, navigate]);

  if (user) return null;

  async function handleSubmit(e) {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const data = await login(username, password, pendingQuiz);
      onAuth(data.token);
      navigate("/dashboard");
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="auth-gate-page auth-gate-page--single">
      <section className="auth-gate-form-wrap">
        <h2 className="auth-title">Sign in</h2>
        <form onSubmit={handleSubmit} className="auth-form">
          {error && <div className="error-banner">{error}</div>}
          <div className="form-group">
            <label className="form-label" htmlFor="login-user">
              Username
            </label>
            <input
              id="login-user"
              className="form-input"
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
              autoFocus
            />
          </div>
          <div className="form-group">
            <label className="form-label" htmlFor="login-pass">
              Password
            </label>
            <input
              id="login-pass"
              className="form-input"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <button
            className="btn btn-primary"
            type="submit"
            disabled={loading}
          >
            {loading ? "Saving..." : "Save your results"}
          </button>
        </form>
        <p className="auth-switch">
          Don&apos;t have an account?{" "}
          <Link to="/register" state={{ pendingQuiz }}>
            Unlock full analysis
          </Link>
        </p>
      </section>
    </div>
  );
}
