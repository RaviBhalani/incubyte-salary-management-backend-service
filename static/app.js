/* ─────────────────────────────────────────
   Step 4.1 — Config & Token Utilities
   ───────────────────────────────────────── */

const ENDPOINTS = {
  login:          '/api/v1/login/',
  refresh:        '/api/v1/token-refresh/',
  employees:      '/api/v1/employee/',
  salaryInsights: '/api/v1/employee/salary-insights/',
};

const PAGE_SIZE = 25;

// ── localStorage helpers ──────────────────

function getAccessToken()  { return localStorage.getItem('access'); }
function getRefreshToken() { return localStorage.getItem('refresh'); }

function saveTokens(access, refresh) {
  localStorage.setItem('access', access);
  localStorage.setItem('refresh', refresh);
}

function clearTokens() {
  localStorage.removeItem('access');
  localStorage.removeItem('refresh');
}

// ── Section toggle helpers ────────────────

function showLogin() {
  document.getElementById('login-section').style.display = '';
  document.getElementById('app-section').style.display   = 'none';
}

function showApp() {
  document.getElementById('login-section').style.display = 'none';
  document.getElementById('app-section').style.display   = '';
}
