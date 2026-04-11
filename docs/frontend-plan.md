# Frontend Implementation Plan

## Context

Adding a minimal single-page frontend to the existing Django REST API salary management project.

**Approach**: Django Templates + plain HTML/CSS/JS. Bootstrap 5 loaded via CDN. No npm, no Node.js, no build step. Frontend and backend live in the same repo and are served from the same origin.

**Correction from original brief**: The login field is `email` (not `username`) because `USERNAME_FIELD = 'email'` on the custom User model. simplejwt derives the field name from `USERNAME_FIELD`, so the login request body must use `{ "email": ..., "password": ... }`.

---

## API Endpoints

| Action | Method | Path |
|--------|--------|------|
| Login | POST | `/api/v1/login/` |
| Refresh token | POST | `/api/v1/token-refresh/` |
| Employee list | GET | `/api/v1/employee/` |
| Employee create | POST | `/api/v1/employee/` |
| Employee retrieve | GET | `/api/v1/employee/{id}/` |
| Employee update | PATCH | `/api/v1/employee/{id}/` |
| Salary insights | GET | `/api/v1/employee/salary-insights/` |

**Supported query params** (employee list + salary insights share the same filter set):

| Param | Type | Description |
|-------|------|-------------|
| `search` | string | Matches `employee_id`, `name`, `email` |
| `job_title` | string | Exact match (TextChoices) |
| `department` | string | Exact match (TextChoices) |
| `country` | string | Exact match (TextChoices) |
| `salary_min` | number | Minimum salary (RangeFilter) |
| `salary_max` | number | Maximum salary (RangeFilter) |
| `page` | number | Omit to return all records (pagination is opt-in) |

**Soft delete**: `PATCH /api/v1/employee/{id}/` with `{ "is_active": false }`. `is_active` is writable via `EmployeeUpdateSerializer`. Deactivated employees are excluded from all list queries (queryset always filters `is_active=True`). There is no DELETE endpoint.

**Employee HTTP methods**: `GET`, `POST`, `PATCH` only.

---

## Files to Create / Modify

| File | Action | Purpose |
|------|--------|---------|
| `incubyte_salary_management_backend_service/settings.py` | Modify | Add `templates/` to TEMPLATES DIRS; add STATICFILES_DIRS |
| `incubyte_salary_management_backend_service/urls.py` | Modify | Add root `''` path serving the SPA shell via TemplateView |
| `templates/index.html` | Create | Single-page app shell |
| `static/app.js` | Create | All fetch calls, auth logic, DOM rendering |
| `static/style.css` | Create | Minor Bootstrap overrides |

---

## Step-by-Step Implementation

### Step 1 — Settings

**File**: `incubyte_salary_management_backend_service/settings.py`

Change TEMPLATES DIRS from `[]` to:
```python
"DIRS": [BASE_DIR / "templates"],
```

Add STATICFILES_DIRS (after STATIC_ROOT):
```python
STATICFILES_DIRS = [BASE_DIR / "static"]
```

`BASE_DIR` already resolves to the repo root in settings.py.

---

### Step 2 — Root URL

**File**: `incubyte_salary_management_backend_service/urls.py`

Add import and a catch-all route at `''` at the **end** of urlpatterns (so it does not shadow existing `/api/v1/` routes). This is a plain Django view — DRF's `IsAuthenticated` permission does not apply:

```python
from django.views.generic import TemplateView

# At the end of urlpatterns:
path("", TemplateView.as_view(template_name="index.html")),
```

---

### Step 3 — `templates/index.html`

Single HTML file. Two top-level sections toggled by JS:

```
<head>
  Bootstrap 5 CSS (CDN — jsdelivr)
  {% load static %}
  <link rel="stylesheet" href="{% static 'style.css' %}">

<body>

  <!-- Login Section (visible when not authenticated) -->
  #login-section
    Centered card with:
    - email input
    - password input
    - Submit button
    - Error message div

  <!-- App Section (hidden until login succeeds) -->
  #app-section  [style="display:none"]

    Navbar: "Salary Management" title + Logout button

    <!-- Salary Insights Cards (4 Bootstrap cards) -->
    #insights-section
      min_salary | max_salary | avg_salary | total_employees

    <!-- Filter + Search Panel -->
    #filter-section
      text input      → ?search=
      select          → ?job_title=   (SOFTWARE_ENGINEER, SENIOR_SOFTWARE_ENGINEER, ENGINEERING_MANAGER, DATA_ANALYST, PRODUCT_MANAGER, HR_MANAGER)
      select          → ?department=  (ENGINEERING, MANAGEMENT, HR)
      select          → ?country=     (UNITED_STATES, INDIA, UNITED_KINGDOM, GERMANY, CANADA, AUSTRALIA)
      number inputs   → ?salary_min= / ?salary_max=
      Apply button + Clear button

    <!-- Employee Table -->
    "Create Employee" button  → opens #create-modal
    #employee-table: thead + tbody (Edit button per row)
    Pagination: prev / next

  <!-- Create Employee Modal (Bootstrap modal) -->
  #create-modal
    Fields: name, job_title, department, salary, joining_date, country

  <!-- Edit Employee Modal (Bootstrap modal) -->
  #edit-modal
    Same fields pre-filled + "Deactivate" button (sends is_active: false)

  Bootstrap 5 JS (CDN — jsdelivr)
  <script src="{% static 'app.js' %}"></script>
```

---

### Step 4 — `static/app.js`

---

#### Step 4.1 — Config & Token Utilities

**Config constants**
```js
const ENDPOINTS = {
  login:          '/api/v1/login/',
  refresh:        '/api/v1/token-refresh/',
  employees:      '/api/v1/employee/',
  salaryInsights: '/api/v1/employee/salary-insights/',
};
const PAGE_SIZE = 25;
```

**localStorage helpers** — pure get/set/clear, no logic:
- `getAccessToken()` / `getRefreshToken()` — read from `localStorage`
- `saveTokens(access, refresh)` — write both keys
- `clearTokens()` — remove both keys

**Section toggle helpers**:
- `showLogin()` — show `#login-section`, hide `#app-section`
- `showApp()` — hide `#login-section`, show `#app-section`

---

#### Step 4.2 — Auth Flow

**`login(email, password)`**
- POST `{ email, password }` to login endpoint with `Content-Type: application/json`
- Happy path: save tokens → `showApp()` → `loadAll()`
- Error — invalid credentials (400/401): extract first message from `error_list` and display it in `#login-error`
- Error — network failure: show "Unable to reach server. Please try again." in `#login-error`
- Always re-enable the submit button after the call resolves

**`logout()`**
- `clearTokens()` → `showLogin()`
- Clear `#login-error` so it doesn't linger on next login attempt

**`authFetch(url, options)`**
- Attaches `Authorization: Bearer <access_token>` header to every request
- On 401: attempts silent token refresh (POST `{ refresh }` to refresh endpoint)
  - Refresh succeeds: save new access token, retry original request once
  - Refresh fails (400/401 or network error): call `logout()` and show a one-time "Your session has expired. Please log in again." message in `#login-error`
- On any other non-2xx: return the response as-is so callers can handle it
- On network error (`fetch` throws): re-throw so callers can show a generic error

---

#### Step 4.3 — Data Fetchers

All functions use `authFetch` and return the parsed JSON response body. Callers handle errors.

- `fetchEmployees(params)` — GET `ENDPOINTS.employees + '?' + buildQueryString(params)`
- `fetchSalaryInsights(params)` — GET `ENDPOINTS.salaryInsights + '?' + buildQueryString(params)`
- `createEmployee(data)` — POST `ENDPOINTS.employees` with JSON body
- `updateEmployee(id, data)` — PATCH `ENDPOINTS.employees + id + '/'` with JSON body

---

#### Step 4.4 — State & Query Builder

**State** — single module-level object:
```js
const currentFilters = {
  search: '', job_title: '', department: '', country: '',
  salary_min: '', salary_max: '', page: 1,
};
```

**`buildQueryString(filters)`**
- Iterate entries, skip blank/null/undefined values and `page: 1` (omitting `page` returns all results per the API's opt-in pagination — only include `page` when `> 1`)
- Return a `URLSearchParams`-encoded string

---

#### Step 4.5 — UI Renderers

**`renderInsightsCards(data)`**
- Populate `#insight-min`, `#insight-max`, `#insight-avg` using `toLocaleString()` for number formatting (e.g. `1,234,567`)
- Populate `#insight-total` as a plain integer
- Edge case — null/undefined values (e.g. no employees match filters): display `—` instead of `null`

**`renderEmployeeTable(employees)`**
- Build `<tr>` per employee: `employee_id`, `name`, `email`, `job_title`, `department`, `country`, salary (formatted with `toLocaleString()`), `joining_date`, Edit button
- Empty state — `employees` is an empty array: render a single `<tr><td colspan="9" class="text-center text-muted">No employees found.</td></tr>`
- Loading state — called with `null` before fetch resolves: render a single row with "Loading…" (reuse what the HTML already has)
- Each Edit button carries `data-id` and a `data-employee` attribute (JSON-encoded row data) for pre-filling the modal

**`renderPagination(count, currentPage)`**
- Update `#pagination-info` text: `Showing page X · Y total employees`
- Disable Prev button when `currentPage === 1`
- Disable Next button when `currentPage * PAGE_SIZE >= count`
- Edge case — `count` is 0: hide the pagination section entirely

---

#### Step 4.6 — Event Wiring & `loadAll()`

**`loadAll()`**
- Set table to loading state (`renderEmployeeTable(null)`)
- Fire `fetchEmployees` and `fetchSalaryInsights` in parallel with `Promise.all` using current filters
- On success: call `renderEmployeeTable`, `renderInsightsCards`, `renderPagination`
- On any error (network or non-2xx): render error row in table — "Failed to load employees. Please refresh." — and reset insight cards to `—`

**Job title → department auto-fill** (applied to both Create and Edit modals)
- Wire `change` on each `.job-title-select`; on change, auto-select the corresponding `.dept-select` value using the map:
  ```
  SOFTWARE_ENGINEER, SENIOR_SOFTWARE_ENGINEER, DATA_ANALYST → ENGINEERING
  ENGINEERING_MANAGER, PRODUCT_MANAGER              → MANAGEMENT
  HR_MANAGER                                        → HR
  ```
- Department remains editable — auto-fill is a convenience, not a lock

**Event bindings (all inside `DOMContentLoaded`)**

| Event | Element | Action |
|-------|---------|--------|
| `submit` | `#login-form` | `preventDefault`, disable button, call `login()` |
| `click` | `#logout-btn` | `logout()` |
| `click` | `#apply-filters-btn` | Read filter inputs → `currentFilters`, reset page to 1, `loadAll()` |
| `click` | `#clear-filters-btn` | Reset all filter inputs + `currentFilters`, `loadAll()` |
| `input` | `#filter-search` | Debounced 400 ms → update `currentFilters.search`, reset page to 1, `loadAll()` |
| `click` | `#prev-page-btn` | `currentFilters.page--`, `loadAll()` |
| `click` | `#next-page-btn` | `currentFilters.page++`, `loadAll()` |
| `submit` | `#create-form` | `preventDefault`, call `createEmployee()`, on success close modal + `loadAll()`, on error display `error_list` in `#create-error` |
| `submit` | `#edit-form` | `preventDefault`, call `updateEmployee()`, on success close modal + `loadAll()`, on error display `error_list` in `#edit-error` |
| `click` | `#deactivate-btn` | `confirm("Deactivate this employee?")` → on confirm call `updateEmployee(id, { is_active: false })`, close modal, `loadAll()` |
| `click` | `#employee-tbody` (delegated) | If `event.target` is an Edit button, pre-fill `#edit-form` from `data-employee`, set `#edit-employee-id`, open modal |
| `change` | `.job-title-select` (both modals) | Auto-fill department |

**Init on page load**
- If `getAccessToken()` exists → `showApp()` + `loadAll()`
- Else → `showLogin()`

---

### Step 5 — `static/style.css`

Minor overrides only:
- Center `#login-section` vertically and horizontally (full-height flex)
- Any card or table spacing tweaks over Bootstrap defaults

---

## Verification

```bash
# Start local stack
./run_server.sh local

# Visit in browser
http://localhost:<port>/

# Checklist:
# 1. Login page appears on first load
# 2. Login with email + password stores tokens in localStorage
# 3. Salary insights cards show aggregated values
# 4. Employee table loads with paginated data
# 5. Filters + search update both table and insights cards simultaneously
# 6. Create employee modal submits and new record appears in table
# 7. Edit employee modal opens pre-filled and saves changes
# 8. Deactivate button removes employee from table
# 9. Token refresh works transparently on 401 (test by clearing access token in DevTools)
# 10. Logout clears localStorage and returns to login page
# 11. No 404s for static assets (app.js, style.css)
```
