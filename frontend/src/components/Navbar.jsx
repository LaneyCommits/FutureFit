import { Link } from "react-router-dom";
import Logo from "./brand/Logo";

export default function Navbar({ user, onLogout }) {
  return (
    <header className="navbar">
      <div className="navbar-inner">
        <Link to="/" className="navbar-brand-link">
          <Logo layout="horizontal" wordmarkSize="sm" />
        </Link>
        <nav className="navbar-nav">
          <Link to="/quiz" className="btn btn-sm btn-ghost">
            Quiz
          </Link>
          <Link to="/about" className="btn btn-sm btn-ghost">
            About
          </Link>
          <Link to="/careers" className="btn btn-sm btn-ghost">
            Careers
          </Link>
          {user ? (
            <>
              <span className="navbar-user">{user.username}</span>
              <button
                type="button"
                className="btn btn-sm btn-ghost"
                onClick={onLogout}
              >
                Log out
              </button>
            </>
          ) : (
            <>
              <Link to="/login" className="btn btn-sm btn-ghost">
                Log in
              </Link>
              <Link to="/register" className="btn btn-sm btn-primary">
                Sign up
              </Link>
            </>
          )}
        </nav>
      </div>
    </header>
  );
}
