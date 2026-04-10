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

/* ─────────────────────────────────────────
   Step 4.2 — Auth Flow
   ───────────────────────────────────────── */

// ── login ─────────────────────────────────

async function login(email, password) {
  const submitBtn  = document.querySelector('#login-form button[type="submit"]');
  const errorEl    = document.getElementById('login-error');

  submitBtn.disabled = true;
  errorEl.classList.add('d-none');
  errorEl.textContent = '';

  try {
    const res  = await fetch(ENDPOINTS.login, {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify({ email, password }),
    });
    const body = await res.json();

    if (res.ok) {
      saveTokens(body.data.access, body.data.refresh);
      showApp();
      loadAll();
    } else {
      const msg = body.error_list?.[0] ?? 'Invalid credentials.';
      errorEl.textContent = typeof msg === 'object' ? Object.values(msg)[0] : msg;
      errorEl.classList.remove('d-none');
    }
  } catch {
    errorEl.textContent = 'Unable to reach server. Please try again.';
    errorEl.classList.remove('d-none');
  } finally {
    submitBtn.disabled = false;
  }
}

// ── logout ────────────────────────────────

function logout() {
  clearTokens();
  document.getElementById('login-error').classList.add('d-none');
  document.getElementById('login-error').textContent = '';
  showLogin();
}

// ── authFetch ─────────────────────────────
// Wraps fetch with a Bearer token. On 401 it attempts a silent token refresh
// and retries once. On second 401 (or refresh failure) it logs the user out.

async function authFetch(url, options = {}) {
  const makeHeaders = () => ({
    'Content-Type': 'application/json',
    ...options.headers,
    'Authorization': `Bearer ${getAccessToken()}`,
  });

  let res = await fetch(url, { ...options, headers: makeHeaders() });

  if (res.status !== 401) return res;

  // ── silent token refresh ──────────────────
  let refreshed = false;
  try {
    const refreshRes  = await fetch(ENDPOINTS.refresh, {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify({ refresh: getRefreshToken() }),
    });
    if (refreshRes.ok) {
      const refreshBody = await refreshRes.json();
      saveTokens(refreshBody.data.access, refreshBody.data.refresh ?? getRefreshToken());
      refreshed = true;
    }
  } catch {
    // network error during refresh — fall through to logout
  }

  if (!refreshed) {
    logout();
    const errorEl = document.getElementById('login-error');
    errorEl.textContent = 'Your session has expired. Please log in again.';
    errorEl.classList.remove('d-none');
    return null;
  }

  // Retry original request once with new access token
  res = await fetch(url, { ...options, headers: makeHeaders() });
  if (res.status === 401) {
    logout();
    const errorEl = document.getElementById('login-error');
    errorEl.textContent = 'Your session has expired. Please log in again.';
    errorEl.classList.remove('d-none');
    return null;
  }
  return res;
}

/* ─────────────────────────────────────────
   Step 4.3 — Data Fetchers
   ───────────────────────────────────────── */

async function fetchEmployees(params) {
  const res = await authFetch(`${ENDPOINTS.employees}?${buildQueryString(params)}`);
  if (!res) return null;
  return res.json();
}

async function fetchSalaryInsights(params) {
  const res = await authFetch(`${ENDPOINTS.salaryInsights}?${buildQueryString(params)}`);
  if (!res) return null;
  return res.json();
}

async function createEmployee(data) {
  const res = await authFetch(ENDPOINTS.employees, {
    method: 'POST',
    body:   JSON.stringify(data),
  });
  if (!res) return null;
  return res.json();
}

async function updateEmployee(id, data) {
  const res = await authFetch(`${ENDPOINTS.employees}${id}/`, {
    method: 'PATCH',
    body:   JSON.stringify(data),
  });
  if (!res) return null;
  return res.json();
}

/* ─────────────────────────────────────────
   Step 4.4 — State & Query Builder
   ───────────────────────────────────────── */

const currentFilters = {
  search: '', job_title: '', department: '', country: '',
  salary_min: '', salary_max: '', page: 1,
};

function buildQueryString(filters) {
  const params = new URLSearchParams();
  for (const [key, value] of Object.entries(filters)) {
    if (value === '' || value === null || value === undefined) continue;
    if (key === 'page' && value === 1) continue;
    params.append(key, value);
  }
  return params.toString();
}

/* ─────────────────────────────────────────
   Step 4.5 — UI Renderers
   ───────────────────────────────────────── */

// ── Insights cards ────────────────────────

function renderInsightsCards(data) {
  const fmt = (val) => (val != null ? Number(val).toLocaleString() : '—');
  document.getElementById('insight-min').textContent   = fmt(data?.min_salary);
  document.getElementById('insight-max').textContent   = fmt(data?.max_salary);
  document.getElementById('insight-avg').textContent   = fmt(data?.avg_salary);
  document.getElementById('insight-total').textContent = data?.total_employees ?? '—';
}

function resetInsightsCards() {
  ['insight-min', 'insight-max', 'insight-avg', 'insight-total'].forEach(
    (id) => (document.getElementById(id).textContent = '—'),
  );
}

// ── Employee table ────────────────────────

function renderEmployeeTable(employees) {
  const tbody = document.getElementById('employee-tbody');

  if (employees === null) {
    tbody.innerHTML = '<tr><td colspan="9" class="text-center text-muted py-4">Loading\u2026</td></tr>';
    return;
  }

  if (employees.length === 0) {
    tbody.innerHTML = '<tr><td colspan="9" class="text-center text-muted py-4">No employees found.</td></tr>';
    return;
  }

  tbody.innerHTML = employees.map((emp) => `
    <tr>
      <td>${emp.employee_id}</td>
      <td>${escapeHtml(emp.name)}</td>
      <td>${escapeHtml(emp.email)}</td>
      <td>${escapeHtml(emp.job_title)}</td>
      <td>${escapeHtml(emp.department)}</td>
      <td>${escapeHtml(emp.country)}</td>
      <td class="text-end">${Number(emp.salary).toLocaleString()}</td>
      <td>${emp.joining_date}</td>
      <td>
        <button
          class="btn btn-outline-primary btn-sm edit-btn"
          data-id="${emp.id}"
          data-employee="${escapeAttr(JSON.stringify(emp))}"
        >Edit</button>
      </td>
    </tr>
  `).join('');
}

// ── Pagination ────────────────────────────

function renderPagination(count, currentPage) {
  const section  = document.getElementById('pagination-section');
  const infoEl   = document.getElementById('pagination-info');
  const prevBtn  = document.getElementById('prev-page-btn');
  const nextBtn  = document.getElementById('next-page-btn');

  if (count === 0) {
    section.style.display = 'none';
    return;
  }

  section.style.display  = '';
  infoEl.textContent     = `Page ${currentPage} · ${count.toLocaleString()} total employees`;
  prevBtn.disabled       = currentPage === 1;
  nextBtn.disabled       = currentPage * PAGE_SIZE >= count;
}

// ── Escape helpers ────────────────────────

function escapeHtml(str) {
  return String(str ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function escapeAttr(str) {
  return String(str ?? '').replace(/"/g, '&quot;');
}
