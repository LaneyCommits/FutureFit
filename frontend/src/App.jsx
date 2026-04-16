import { useEffect } from "react";
import { BrowserRouter, Navigate, Route, Routes, useLocation } from "react-router-dom";
import Navbar from "./components/Navbar";
import Landing from "./pages/Landing";
import Quiz from "./pages/Quiz";
import Results from "./pages/Results";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import About from "./pages/About";
import Careers from "./pages/Careers";
import useAuth from "./hooks/useAuth";

function AppRoutes({ user, saveToken, logout }) {
  const location = useLocation();
  const immersiveRoutes = ["/", "/quiz"];
  const hideNav = immersiveRoutes.includes(location.pathname);
  const seoMap = {
    "/": {
      title: "ExploringU | Career Path Quiz for Students",
      description:
        "ExploringU helps students explore career paths that match their strengths and tendencies through a short, personalized assessment.",
    },
    "/quiz": {
      title: "Career Quiz for Students | ExploringU",
      description:
        "Take a short college major and career path assessment to discover career directions that align with your strengths.",
    },
    "/about": {
      title: "About ExploringU | Student Career Path Assessment",
      description:
        "Learn how ExploringU helps students answer what career fits me through a clear, strengths-based assessment process.",
    },
    "/careers": {
      title: "Career Paths and Majors | ExploringU",
      description:
        "Explore career path categories and major directions designed for students deciding what to study and where to grow.",
    },
  };

  useEffect(() => {
    const fallback = {
      title: "ExploringU | Career Path Quiz for Students",
      description:
        "ExploringU helps students explore career paths that match their strengths and tendencies through a short, personalized assessment.",
    };
    const config = seoMap[location.pathname] || fallback;
    document.title = config.title;

    const descriptionTag = document.querySelector('meta[name="description"]');
    if (descriptionTag) {
      descriptionTag.setAttribute("content", config.description);
    }

    const canonicalTag = document.querySelector('link[rel="canonical"]');
    if (canonicalTag) {
      canonicalTag.setAttribute("href", `https://exploringu.com${location.pathname}`);
    }

    const ogTitleTag = document.querySelector('meta[property="og:title"]');
    if (ogTitleTag) ogTitleTag.setAttribute("content", config.title);

    const ogDescriptionTag = document.querySelector('meta[property="og:description"]');
    if (ogDescriptionTag) ogDescriptionTag.setAttribute("content", config.description);

    const ogUrlTag = document.querySelector('meta[property="og:url"]');
    if (ogUrlTag) ogUrlTag.setAttribute("content", `https://exploringu.com${location.pathname}`);
  }, [location.pathname]);

  return (
    <div className="page-shell">
      {!hideNav && <Navbar user={user} onLogout={logout} />}
      <main className="page-main">
        <Routes>
          <Route path="/" element={<Landing user={user} />} />
          <Route path="/quiz" element={<Quiz />} />
          <Route path="/about" element={<About />} />
          <Route path="/careers" element={<Careers />} />
          <Route path="/results" element={<Results user={user} />} />
          <Route path="/login" element={<Login onAuth={saveToken} user={user} />} />
          <Route
            path="/register"
            element={<Register onAuth={saveToken} user={user} />}
          />
          <Route
            path="/dashboard"
            element={user ? <Dashboard /> : <Navigate to="/login" replace />}
          />
        </Routes>
      </main>
    </div>
  );
}

export default function App() {
  const { user, loading, saveToken, logout } = useAuth();

  if (loading) {
    return (
      <div className="page-center">
        <div className="loading-spinner" />
      </div>
    );
  }

  return (
    <BrowserRouter>
      <AppRoutes user={user} saveToken={saveToken} logout={logout} />
    </BrowserRouter>
  );
}
