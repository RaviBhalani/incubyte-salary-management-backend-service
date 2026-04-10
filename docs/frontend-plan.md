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

**CONFIG**
```js
const ENDPOINTS = {
  login:          '/api/v1/login/',
  refresh:        '/api/v1/token-refresh/',
  employees:      '/api/v1/employee/',
  salaryInsights: '/api/v1/employee/salary-insights/',
};
```

**Auth helpers**
- `getAccessToken()` / `getRefreshToken()` — read from `localStorage`
- `saveTokens(access, refresh)` — write to `localStorage`
- `clearTokens()` — remove from `localStorage`
- `login(email, password)` — POST to login endpoint, save tokens, show app, call `loadAll()`
- `logout()` — `clearTokens()`, show login section
- `authFetch(url, options)` — wraps `fetch` with `Authorization: Bearer` header; on 401, tries token refresh and retries once; on second 401, calls `logout()`

**Data fetchers**
- `fetchEmployees(params)` — `authFetch` GET `/api/v1/employee/` with query string
- `createEmployee(data)` — `authFetch` POST `/api/v1/employee/`
- `updateEmployee(id, data)` — `authFetch` PATCH `/api/v1/employee/{id}/`
- `fetchSalaryInsights(params)` — `authFetch` GET `/api/v1/employee/salary-insights/` with same params

**UI renderers**
- `renderInsightsCards(data)` — populate 4 card values
- `renderEmployeeTable(employees)` — build tbody rows; each row has Edit button
- `renderPagination(count, currentPage)` — simple prev/next controls
- `buildQueryString(filters)` — serialize filter state to URL query string

**State**: single `currentFilters` object (filter values + current page)

**Event wiring (on `DOMContentLoaded`)**
- Login form submit → `login()`
- Logout button → `logout()`
- Apply Filters → reset page to 1, `loadAll()`
- Clear button → reset all filters, `loadAll()`
- Search input (debounced 400 ms) → `loadAll()`
- Pagination prev/next → adjust page, `loadAll()`
- Create modal submit → `createEmployee()`, close modal, `loadAll()`
- Edit modal submit → `updateEmployee()`, close modal, `loadAll()`
- Edit modal Deactivate → `updateEmployee(id, { is_active: false })`, close modal, `loadAll()`
- Edit button click (delegated on tbody) → open edit modal pre-filled

**`loadAll()`** — calls `fetchEmployees` + `fetchSalaryInsights` in parallel with current filters, then calls `renderEmployeeTable` + `renderInsightsCards`.

**Init on page load**: if `getAccessToken()` exists → show app + `loadAll()`; else → show login.

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
