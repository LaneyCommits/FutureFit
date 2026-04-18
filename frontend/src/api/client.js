const BASE_URL = import.meta.env.VITE_API_URL || "";

async function request(endpoint, options = {}) {
  const url = `${BASE_URL}${endpoint}`;
  const headers = { "Content-Type": "application/json", ...options.headers };

  const token = localStorage.getItem("token");
  if (token) {
    headers["Authorization"] = `Token ${token}`;
  }

  const res = await fetch(url, { ...options, headers });
  const data = await res.json();

  if (!res.ok) {
    const message = data.error || data.detail || JSON.stringify(data);
    throw new Error(message);
  }

  return data;
}

/** Single fetch — backend always returns exactly 10 questions. */
export function getQuestions() {
  return request("/api/quiz/questions/");
}

/** Submit exactly 10 choice keys in question order (no short/long flag). */
export function submitQuiz(answers) {
  return request("/api/quiz/submit/", {
    method: "POST",
    body: JSON.stringify({ answers }),
  });
}

export function register(username, password, pendingQuiz = null) {
  return request("/api/users/register/", {
    method: "POST",
    body: JSON.stringify({
      username,
      password,
      ...(pendingQuiz ? { pending_quiz: pendingQuiz } : {}),
    }),
  });
}

export function login(username, password, pendingQuiz = null) {
  return request("/api/users/login/", {
    method: "POST",
    body: JSON.stringify({
      username,
      password,
      ...(pendingQuiz ? { pending_quiz: pendingQuiz } : {}),
    }),
  });
}

export function getMe() {
  return request("/api/users/me/");
}

export function getDashboard() {
  return request("/api/users/dashboard/");
}

/** Authenticated POST to /api/insights/<path>/ */
export function postInsight(path, body) {
  const safe = String(path || "").replace(/^\/+|\/+$/g, "");
  return request(`/api/insights/${safe}/`, {
    method: "POST",
    body: JSON.stringify(body ?? {}),
  });
}

export function getCareerJobs(limit = 80) {
  const n = Math.max(1, Math.min(200, Number(limit) || 80));
  return request(`/api/careers/jobs/?limit=${n}`);
}
