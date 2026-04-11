/* ─────────────────────────────────────────
   Step 4.1 — Config & Token Utilities
   ───────────────────────────────────────── */

const ENDPOINTS = {
  login:          '/api/v1/login/',
  refresh:        '/api/v1/token-refresh/',
  logout:         '/api/v1/logout/',
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

async function logout() {
  try {
    await fetch(ENDPOINTS.logout, {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify({ refresh: getRefreshToken() }),
    });
  } catch {
    // best-effort — always clear local tokens regardless of server response
  }
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
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

async function fetchSalaryInsights(params) {
  const res = await authFetch(`${ENDPOINTS.salaryInsights}?${buildQueryString(params)}`);
  if (!res) return null;
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
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
  salary_min: '', salary_max: '', page: 1, page_size: 25,
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
      <td>${escapeHtml(formatLabel(emp.job_title))}</td>
      <td>${escapeHtml(formatLabel(emp.department))}</td>
      <td>${escapeHtml(formatLabel(emp.country))}</td>
      <td>$${Number(emp.salary).toLocaleString()}</td>
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
  const infoEl  = document.getElementById('pagination-info');
  const prevBtn = document.getElementById('prev-page-btn');
  const nextBtn = document.getElementById('next-page-btn');

  infoEl.textContent = `Page ${currentPage} · ${count.toLocaleString()} total employees`;
  prevBtn.disabled                                             = currentPage === 1;
  nextBtn.disabled                                             = count === 0 || currentPage * currentFilters.page_size >= count;
  document.getElementById('page-size-select').disabled        = count === 0;
}

// ── Escape helpers ────────────────────────

function formatLabel(value) {
  return String(value ?? '')
    .split('_')
    .map((word) => word.length <= 2
      ? word.toUpperCase()
      : word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
    .join(' ');
}

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

const DEPARTMENT_JOB_TITLES_MAP = {
  ENGINEERING: [
    { value: 'SOFTWARE_ENGINEER',        label: 'Software Engineer' },
    { value: 'SENIOR_SOFTWARE_ENGINEER', label: 'Senior Software Engineer' },
    { value: 'DATA_ANALYST',             label: 'Data Analyst' },
  ],
  MANAGEMENT: [
    { value: 'ENGINEERING_MANAGER', label: 'Engineering Manager' },
    { value: 'PRODUCT_MANAGER',     label: 'Product Manager' },
  ],
  HR: [
    { value: 'HR_MANAGER', label: 'HR Manager' },
  ],
};

function validateSalaryInput(inputEl) {
  const val = Number(inputEl.value);
  const outOfRange = inputEl.value !== '' && (val < 10000 || val > 1000000);
  inputEl.classList.toggle('is-invalid', outOfRange);
  return outOfRange;
}

function populateModalJobTitles(deptValue, jobTitleSelect) {
  if (!deptValue) {
    jobTitleSelect.innerHTML = '<option value="">Select a department first</option>';
    jobTitleSelect.disabled  = true;
    return;
  }
  const titles = DEPARTMENT_JOB_TITLES_MAP[deptValue] ?? [];
  jobTitleSelect.innerHTML =
    '<option value="">Select\u2026</option>' +
    titles.map((t) => `<option value="${t.value}">${t.label}</option>`).join('');
  jobTitleSelect.disabled = false;
}

function populateFilterJobTitles(department) {
  const select = document.getElementById('filter-job-title');
  const titles = department
    ? (DEPARTMENT_JOB_TITLES_MAP[department] ?? [])
    : Object.values(DEPARTMENT_JOB_TITLES_MAP).flat();
  select.innerHTML =
    '<option value="">All</option>' +
    titles.map((t) => `<option value="${t.value}">${t.label}</option>`).join('');
  select.value = '';
}

// ── loadAll ───────────────────────────────

async function loadAll() {
  renderEmployeeTable(null);

  try {
    const { page: _page, page_size: _page_size, ...insightFilters } = currentFilters;
    const [empBody, insightsBody] = await Promise.all([
      fetchEmployees(currentFilters),
      fetchSalaryInsights(insightFilters),
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
  populateFilterJobTitles('');
  const maxEl = document.getElementById('filter-salary-max');
  maxEl.nextElementSibling.textContent = '10,000 \u2013 1,000,000';
  ['filter-salary-min', 'filter-salary-max'].forEach(
    (id) => document.getElementById(id).classList.remove('is-invalid'),
  );
  document.getElementById('apply-filters-btn').disabled = false;
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

function showToast(message) {
  document.getElementById('success-toast-body').textContent = message;
  bootstrap.Toast.getOrCreateInstance(document.getElementById('success-toast')).show();
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
  form.querySelector('[name="department"]').value   = emp.department;
  const jobTitleSelect = form.querySelector('[name="job_title"]');
  populateModalJobTitles(emp.department, jobTitleSelect);
  jobTitleSelect.value                              = emp.job_title;
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

  // Salary range validation (individual range + cross-validation)
  const updateApplyBtn = () => {
    const minEl = document.getElementById('filter-salary-min');
    const maxEl = document.getElementById('filter-salary-max');
    const maxFeedbackEl = maxEl.nextElementSibling;

    const minInvalid = validateSalaryInput(minEl);
    const maxInvalid = validateSalaryInput(maxEl);

    // Reset cross-validation feedback before re-evaluating
    maxFeedbackEl.textContent = '10,000 \u2013 1,000,000';

    // Cross-validation: both filled, both in range, but min > max
    const crossInvalid =
      minEl.value !== '' && maxEl.value !== '' &&
      !minInvalid && !maxInvalid &&
      Number(minEl.value) > Number(maxEl.value);

    if (crossInvalid) {
      maxEl.classList.add('is-invalid');
      maxFeedbackEl.textContent = 'Must be \u2265 Min Salary';
    }

    document.getElementById('apply-filters-btn').disabled = minInvalid || maxInvalid || crossInvalid;
  };
  document.getElementById('filter-salary-min').addEventListener('input', updateApplyBtn);
  document.getElementById('filter-salary-max').addEventListener('input', updateApplyBtn);

  // Modal salary validation
  ['create-form', 'edit-form'].forEach((formId) => {
    const form        = document.getElementById(formId);
    const salaryInput = form.querySelector('[name="salary"]');
    const submitBtn   = form.querySelector('[type="submit"]');
    salaryInput.addEventListener('input', () => {
      submitBtn.disabled = validateSalaryInput(salaryInput);
    });
  });

  // Department → cascade job title options
  document.getElementById('filter-department').addEventListener('change', () => {
    const dept = document.getElementById('filter-department').value;
    populateFilterJobTitles(dept);
    currentFilters.job_title  = '';
    currentFilters.department = dept;
    currentFilters.page       = 1;
    loadAll();
  });

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

  // Rows per page
  document.getElementById('page-size-select').addEventListener('change', () => {
    currentFilters.page_size = Number(document.getElementById('page-size-select').value);
    currentFilters.page      = 1;
    loadAll();
  });

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
    const form = document.getElementById('create-form');
    form.reset();
    hideModalError('create-error');
    populateModalJobTitles('', form.querySelector('[name="job_title"]'));
    form.querySelector('[name="salary"]').classList.remove('is-invalid');
    form.querySelector('[type="submit"]').disabled = false;
  });

  // Create form submit
  document.getElementById('create-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    hideModalError('create-error');
    const submitBtn = e.target.querySelector('[type="submit"]');
    submitBtn.disabled = true;
    try {
      const body = await createEmployee(getFormData(e.target));
      if (!body) return; // authFetch handled logout
      if (body.error_list?.length) { showModalError('create-error', body.error_list); return; }
      bootstrap.Modal.getInstance(document.getElementById('create-modal')).hide();
      showToast('Employee created successfully.');
      loadAll();
    } finally {
      submitBtn.disabled = false;
    }
  });

  // Edit form submit
  document.getElementById('edit-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    hideModalError('edit-error');
    const submitBtn = e.target.querySelector('[type="submit"]');
    submitBtn.disabled = true;
    try {
      const id   = document.getElementById('edit-employee-id').value;
      const body = await updateEmployee(id, getFormData(e.target));
      if (!body) return;
      if (body.error_list?.length) { showModalError('edit-error', body.error_list); return; }
      bootstrap.Modal.getInstance(document.getElementById('edit-modal')).hide();
      showToast('Employee updated successfully.');
      loadAll();
    } finally {
      submitBtn.disabled = false;
    }
  });

  // Deactivate button — show confirmation modal
  document.getElementById('deactivate-btn').addEventListener('click', () => {
    bootstrap.Modal.getOrCreateInstance(document.getElementById('deactivate-modal')).show();
  });

  document.getElementById('deactivate-modal').addEventListener('show.bs.modal', () => {
    document.getElementById('edit-modal').classList.add('modal-dimmed');
  });
  document.getElementById('deactivate-modal').addEventListener('hidden.bs.modal', () => {
    document.getElementById('edit-modal').classList.remove('modal-dimmed');
    hideModalError('deactivate-error');
  });

  // Confirm deactivation
  document.getElementById('confirm-deactivate-btn').addEventListener('click', async () => {
    const confirmBtn = document.getElementById('confirm-deactivate-btn');
    confirmBtn.disabled = true;
    try {
      const id   = document.getElementById('edit-employee-id').value;
      const body = await updateEmployee(id, { is_active: false });
      if (!body) return; // 401 — already logged out
      if (body.error_list?.length) { showModalError('deactivate-error', body.error_list); return; }
      hideModalError('deactivate-error');
      bootstrap.Modal.getInstance(document.getElementById('deactivate-modal')).hide();
      bootstrap.Modal.getInstance(document.getElementById('edit-modal')).hide();
      showToast('Employee deactivated successfully.');
      loadAll();
    } finally {
      confirmBtn.disabled = false;
    }
  });

  // Edit button — delegated on tbody
  document.getElementById('employee-tbody').addEventListener('click', (e) => {
    const btn = e.target.closest('.edit-btn');
    if (!btn) return;
    let emp;
    try { emp = JSON.parse(btn.dataset.employee); } catch {
      showToast('Could not open employee. Please refresh.');
      return;
    }
    const form = document.getElementById('edit-form');
    prefillEditForm(emp);
    hideModalError('edit-error');
    form.querySelector('[name="salary"]').classList.remove('is-invalid');
    form.querySelector('[type="submit"]').disabled = false;
    bootstrap.Modal.getOrCreateInstance(document.getElementById('edit-modal')).show();
  });

  // Department → cascade job title options (both modals)
  document.querySelectorAll('.modal-dept-select').forEach((select) => {
    select.addEventListener('change', (e) => {
      const jobTitleSelect = e.target.closest('form').querySelector('.modal-job-title-select');
      populateModalJobTitles(e.target.value, jobTitleSelect);
    });
  });

});
