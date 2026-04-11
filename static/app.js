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
      saveTokens(body.access, body.refresh);
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
      saveTokens(refreshBody.access, refreshBody.refresh ?? getRefreshToken());
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
    // always include page so the API returns paginated results (25 per page)
    // rather than all records at once
    params.append(key, value);
  }
  return params.toString();
}

/* ─────────────────────────────────────────
   Step 4.5 — UI Renderers
   ───────────────────────────────────────── */

// ── Insights cards ────────────────────────

function renderInsightsCards(data) {
  const fmt = (val) => (val != null ? '$' + Number(val).toLocaleString() : '—');
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
      <td class="text-end">$${Number(emp.salary).toLocaleString()}</td>
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

/* ─────────────────────────────────────────
   Step 4.6 — Event Wiring & loadAll()
   ───────────────────────────────────────── */

const JOB_TITLE_DEPARTMENT_MAP = {
  SOFTWARE_ENGINEER:        'ENGINEERING',
  SENIOR_SOFTWARE_ENGINEER: 'ENGINEERING',
  DATA_ANALYST:             'ENGINEERING',
  ENGINEERING_MANAGER:      'MANAGEMENT',
  PRODUCT_MANAGER:          'MANAGEMENT',
  HR_MANAGER:               'HR',
};

// ── loadAll ───────────────────────────────

async function loadAll() {
  renderEmployeeTable(null);

  try {
    const [empBody, insightsBody] = await Promise.all([
      fetchEmployees(currentFilters),
      fetchSalaryInsights(currentFilters),
    ]);

    if (!empBody || !insightsBody) return; // authFetch already handled logout

    // Handle both paginated ({ count, results }) and plain-array responses
    const employees = Array.isArray(empBody.data) ? empBody.data : (empBody.data.results ?? []);
    const count     = Array.isArray(empBody.data) ? empBody.data.length : (empBody.data.count ?? 0);

    renderEmployeeTable(employees);
    renderInsightsCards(insightsBody.data);
    renderPagination(count, currentFilters.page);
  } catch {
    document.getElementById('employee-tbody').innerHTML =
      '<tr><td colspan="9" class="text-center text-danger py-4">Failed to load employees. Please refresh.</td></tr>';
    resetInsightsCards();
  }
}

// ── Helpers ───────────────────────────────

function debounce(fn, delay) {
  let timer;
  return (...args) => {
    clearTimeout(timer);
    timer = setTimeout(() => fn(...args), delay);
  };
}

function readFilters() {
  currentFilters.search     = document.getElementById('filter-search').value.trim();
  currentFilters.job_title  = document.getElementById('filter-job-title').value;
  currentFilters.department = document.getElementById('filter-department').value;
  currentFilters.country    = document.getElementById('filter-country').value;
  currentFilters.salary_min = document.getElementById('filter-salary-min').value;
  currentFilters.salary_max = document.getElementById('filter-salary-max').value;
}

function resetFilters() {
  ['filter-search', 'filter-job-title', 'filter-department',
   'filter-country', 'filter-salary-min', 'filter-salary-max'].forEach(
    (id) => (document.getElementById(id).value = ''),
  );
  Object.assign(currentFilters, {
    search: '', job_title: '', department: '', country: '',
    salary_min: '', salary_max: '', page: 1,
  });
}

function getFormData(form) {
  const data = {};
  new FormData(form).forEach((value, key) => {
    if (value !== '') data[key] = value;
  });
  return data;
}

function showModalError(errorElId, errorList) {
  const el  = document.getElementById(errorElId);
  const msg = errorList?.[0] ?? 'Something went wrong.';
  el.textContent = typeof msg === 'object' ? Object.values(msg)[0] : msg;
  el.classList.remove('d-none');
}

function hideModalError(errorElId) {
  const el = document.getElementById(errorElId);
  el.classList.add('d-none');
  el.textContent = '';
}

function prefillEditForm(emp) {
  document.getElementById('edit-employee-id').value           = emp.id;
  const form = document.getElementById('edit-form');
  form.querySelector('[name="name"]').value         = emp.name;
  form.querySelector('[name="job_title"]').value    = emp.job_title;
  form.querySelector('[name="department"]').value   = emp.department;
  form.querySelector('[name="salary"]').value       = emp.salary;
  form.querySelector('[name="joining_date"]').value = emp.joining_date;
  form.querySelector('[name="country"]').value      = emp.country;
}

// ── Event wiring ──────────────────────────

document.addEventListener('DOMContentLoaded', () => {

  // Init: restore session if token exists
  if (getAccessToken()) {
    showApp();
    loadAll();
  } else {
    showLogin();
  }

  // Login form
  document.getElementById('login-form').addEventListener('submit', (e) => {
    e.preventDefault();
    login(
      document.getElementById('login-email').value.trim(),
      document.getElementById('login-password').value,
    );
  });

  // Password show/hide toggle
  document.getElementById('toggle-password').addEventListener('click', () => {
    const passwordInput = document.getElementById('login-password');
    const icon = document.getElementById('toggle-password-icon');
    const isHidden = passwordInput.type === 'password';
    passwordInput.type = isHidden ? 'text' : 'password';
    icon.className = isHidden ? 'bi bi-eye-slash' : 'bi bi-eye';
  });

  // Logout
  document.getElementById('logout-btn').addEventListener('click', logout);

  // Apply filters
  document.getElementById('apply-filters-btn').addEventListener('click', () => {
    readFilters();
    currentFilters.page = 1;
    loadAll();
  });

  // Clear filters
  document.getElementById('clear-filters-btn').addEventListener('click', () => {
    resetFilters();
    loadAll();
  });

  // Search (debounced 400 ms)
  document.getElementById('filter-search').addEventListener(
    'input',
    debounce(() => {
      currentFilters.search = document.getElementById('filter-search').value.trim();
      currentFilters.page   = 1;
      loadAll();
    }, 400),
  );

  // Pagination
  document.getElementById('prev-page-btn').addEventListener('click', () => {
    currentFilters.page--;
    loadAll();
  });

  document.getElementById('next-page-btn').addEventListener('click', () => {
    currentFilters.page++;
    loadAll();
  });

  // Create modal: clear form and errors on open
  document.getElementById('create-modal').addEventListener('show.bs.modal', () => {
    document.getElementById('create-form').reset();
    hideModalError('create-error');
  });

  // Create form submit
  document.getElementById('create-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    hideModalError('create-error');
    const body = await createEmployee(getFormData(e.target));
    if (!body) return; // authFetch handled logout
    if (body.error_list?.length) { showModalError('create-error', body.error_list); return; }
    bootstrap.Modal.getInstance(document.getElementById('create-modal')).hide();
    loadAll();
  });

  // Edit form submit
  document.getElementById('edit-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    hideModalError('edit-error');
    const id   = document.getElementById('edit-employee-id').value;
    const body = await updateEmployee(id, getFormData(e.target));
    if (!body) return;
    if (body.error_list?.length) { showModalError('edit-error', body.error_list); return; }
    bootstrap.Modal.getInstance(document.getElementById('edit-modal')).hide();
    loadAll();
  });

  // Deactivate button
  document.getElementById('deactivate-btn').addEventListener('click', async () => {
    if (!confirm('Deactivate this employee?')) return;
    const id   = document.getElementById('edit-employee-id').value;
    const body = await updateEmployee(id, { is_active: false });
    if (!body) return;
    bootstrap.Modal.getInstance(document.getElementById('edit-modal')).hide();
    loadAll();
  });

  // Edit button — delegated on tbody
  document.getElementById('employee-tbody').addEventListener('click', (e) => {
    const btn = e.target.closest('.edit-btn');
    if (!btn) return;
    prefillEditForm(JSON.parse(btn.dataset.employee));
    hideModalError('edit-error');
    bootstrap.Modal.getOrCreateInstance(document.getElementById('edit-modal')).show();
  });

  // Job title → department auto-fill (both modals)
  document.querySelectorAll('.job-title-select').forEach((select) => {
    select.addEventListener('change', () => {
      const dept = JOB_TITLE_DEPARTMENT_MAP[select.value] ?? '';
      select.closest('form').querySelector('.dept-select').value = dept;
    });
  });

});
