# Frontend Implementation

## Context

A minimal single-page frontend for the Django REST API salary management project.

**Approach**: Django Templates + plain HTML/CSS/JS. Bootstrap 5 loaded via CDN. No npm, no Node.js, no build step. Frontend and backend live in the same repo and are served from the same origin.

**Note**: The login field is `email` (not `username`) because `USERNAME_FIELD = 'email'` on the custom User model. simplejwt derives the field name from `USERNAME_FIELD`, so the login request body uses `{ "email": ..., "password": ... }`.

---

## API Endpoints

| Action | Method | Path |
|--------|--------|------|
| Login | POST | `/api/v1/login/` |
| Refresh token | POST | `/api/v1/token-refresh/` |
| Logout (blacklist) | POST | `/api/v1/logout/` |
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
| `page` | number | Enables pagination; omit to return all records |
| `page_size` | number | Records per page (default 25, max 200) |

**Soft delete**: `PATCH /api/v1/employee/{id}/` with `{ "is_active": false }`. Deactivated employees are excluded from all list queries. There is no DELETE endpoint.

**Employee HTTP methods**: `GET`, `POST`, `PATCH` only.

---

## Files

| File | Purpose |
|------|---------|
| `incubyte_salary_management_backend_service/settings.py` | `templates/` in TEMPLATES DIRS; STATICFILES_DIRS pointing to `static/` |
| `incubyte_salary_management_backend_service/urls.py` | Root `''` path serving the SPA shell via TemplateView |
| `templates/index.html` | Single-page app shell |
| `static/app.js` | All fetch calls, auth logic, DOM rendering |
| `static/style.css` | Minor Bootstrap overrides |

---

## `templates/index.html`

Two top-level sections toggled by JS:

- **`#login-section`** — centered card with email input, password input with show/hide toggle, submit button, error alert
- **`#app-section`** — full dashboard, hidden until login succeeds:
  - Navbar: title + Logout button
  - `#insights-section` — four cards: Min Salary, Max Salary, Avg Salary, Total Employees
  - `#filter-section` — search text input, department select, job title select (cascades from department), country select, salary min/max number inputs, Apply + Clear buttons
  - Employee table with thead + tbody, Edit button per row
  - Pagination: rows-per-page select (25/50/100), Prev/Next buttons, info label
  - `#create-modal` — Bootstrap modal: name, department, job title (cascades), salary, joining date, country
  - `#edit-modal` — same fields pre-filled + Deactivate button in footer
  - `#deactivate-modal` — small confirmation modal stacked over edit modal
  - `#success-toast` — bottom-right Bootstrap toast for success messages

---

## `static/app.js`

### Config & Token Utilities

```js
const ENDPOINTS = {
  login:          '/api/v1/login/',
  refresh:        '/api/v1/token-refresh/',
  logout:         '/api/v1/logout/',
  employees:      '/api/v1/employee/',
  salaryInsights: '/api/v1/employee/salary-insights/',
};
```

**localStorage helpers**: `getAccessToken()`, `getRefreshToken()`, `saveTokens(access, refresh)`, `clearTokens()`.

**Section toggle helpers**: `showLogin()`, `showApp()`.

---

### Auth Flow

**`login(email, password)`**
- Disables submit button for the duration of the call
- POST `{ email, password }` to login endpoint
- Happy path: save tokens → `showApp()` → `loadAll()`
- Error: display all messages from `error_list` in `#login-error` (joined with a space); fallback to `'Invalid credentials.'`
- Network failure: show `'Unable to reach server. Please try again.'`
- Re-enables submit button in `finally`

**`logout()`** _(async)_
- Best-effort POST `{ refresh }` to `/api/v1/logout/` to blacklist the token server-side
- Always calls `clearTokens()` + `showLogin()` regardless of server response (network errors are swallowed)
- Clears `#login-error` so it doesn't linger on the next login attempt

**`authFetch(url, options)`**
- Attaches `Authorization: Bearer <access_token>` to every request
- On 401: attempts silent token refresh (POST `{ refresh }` to refresh endpoint)
  - Refresh succeeds: save new access token (and refresh token if rotated), retry original request once
  - Refresh fails: call `logout()`, show `'Your session has expired.'` in `#login-error`, return `null`
- Returns the `Response` object (success or error) for the caller to handle

---

### Data Fetchers

All use `authFetch`. Return parsed JSON body; throw on non-2xx HTTP.

- `fetchEmployees(params)` — GET employee list with query params
- `fetchSalaryInsights(params)` — GET salary insights with query params
- `fetchEmployee(id)` — GET single employee by ID (`/api/v1/employee/{id}/`); used by the edit button to load fresh data before opening the modal
- `createEmployee(data)` — POST new employee
- `updateEmployee(id, data)` — PATCH employee by ID

---

### State & Query Builder

```js
const currentFilters = {
  search: '', job_title: '', department: '', country: '',
  salary_min: '', salary_max: '', page: 1, page_size: 25,
};
```

**`buildQueryString(filters)`**: Iterates entries, skips blank/null/undefined values, encodes via `URLSearchParams`. `page` is always included (the API uses its presence to enable pagination).

**`readFilters()`**: Reads current DOM values of all filter inputs into `currentFilters`.

**`resetFilters()`**: Clears all filter inputs, resets `currentFilters`, repopulates job title dropdown, removes `is-invalid` state from salary inputs, resets salary max feedback text to `'10,000 – 1,000,000'`.

---

### UI Renderers

**`renderInsightsCards(data)`**: Populates the four cards. Null/undefined values display as `—`. Salary values are prefixed with `$` and formatted with `toLocaleString()`.

**`renderEmployeeTable(employees)`**:
- `null` → Loading… row
- `[]` → No employees found. row
- Array → one `<tr>` per employee. Each Edit button carries `data-id` only (no stale JSON snapshot). All text content is passed through `escapeHtml()`.

**`renderPagination(count, currentPage)`**: Updates info label, disables Prev at page 1, disables Next when `currentPage * page_size >= count`, disables rows-per-page select when count is 0.

**`formatLabel(value)`**: Converts snake_case enum values to Title Case for display (e.g. `SOFTWARE_ENGINEER` → `Software Engineer`).

**`escapeHtml(str)`** / **`escapeAttr(str)`**: XSS-safe string helpers used in all innerHTML construction.

---

### Error Helpers

**`normalizeError(err)`**: Converts an error entry to a string — if the entry is an object, takes the first value; otherwise returns as-is.

**`showModalError(errorElId, errorList)`**:
- Single error → `el.textContent = errors[0]`
- Multiple errors → renders a `<ul>` list using `escapeHtml` for safety
- Fallback when `errorList` is empty → `'Something went wrong.'`

**`hideModalError(errorElId)`**: Adds `d-none` and clears content.

**`showToast(message)`**: Shows the `#success-toast` Bootstrap toast with the given message.

---

### Form Helpers

**`getFormData(form)`**: Collects all named form fields via `FormData` into a plain object. Empty strings are **included** — this ensures clearing a required field sends `""` to the backend and triggers a proper validation error rather than silently preserving the old value.

**`prefillEditForm(emp)`**: Populates the edit modal fields from an employee object. Calls `populateModalJobTitles` to rebuild the job title dropdown for the employee's current department before setting the value.

---

### Salary Filter Validation

**`validateSalaryInput(inputEl)`**: Marks input as `is-invalid` if value is non-empty and outside 10,000–1,000,000. Returns a boolean.

**`updateApplyBtn()`**: Runs both individual range validations, then applies cross-validation:
- If both fields are filled, individually valid, but `min > max` → marks max field invalid with feedback text `'Must be ≥ Min Salary'`
- Resets max feedback text to `'10,000 – 1,000,000'` on every call before re-evaluating
- Disables Apply button if any validation fails

---

### Department → Job Title Cascade

**`populateModalJobTitles(deptValue, jobTitleSelect)`**: Rebuilds the job title `<select>` options for the given department. Disables and resets the select when no department is provided (used in Create modal).

**`populateFilterJobTitles(department)`**: Rebuilds the filter panel job title dropdown. Shows all job titles when no department is selected.

---

### `loadAll()`

1. Sets table to loading state
2. Strips `page` and `page_size` from filters for the insights call (insights are not paginated)
3. Fires `fetchEmployees` and `fetchSalaryInsights` in parallel via `Promise.all`
4. On success: renders table, insights cards, and pagination
5. On error: renders error row in table and resets insight cards to `—`

---

### Event Wiring (inside `DOMContentLoaded`)

| Event | Element | Action |
|-------|---------|--------|
| `submit` | `#login-form` | `preventDefault`, call `login()` |
| `click` | `#logout-btn` | `logout()` |
| `click` | `#toggle-password` | Toggles password input `type` between `password` and `text` |
| `input` | `#filter-salary-min` | `updateApplyBtn()` |
| `input` | `#filter-salary-max` | `updateApplyBtn()` |
| `input` (modal salary) | `[name="salary"]` in create + edit forms | `validateSalaryInput()`; disables submit if invalid |
| `change` | `#filter-department` | Repopulates filter job title dropdown, updates `currentFilters`, resets page, `loadAll()` |
| `click` | `#apply-filters-btn` | `readFilters()`, reset page to 1, `loadAll()` |
| `click` | `#clear-filters-btn` | `resetFilters()`, `loadAll()` |
| `input` | `#filter-search` | Debounced 400 ms → update `currentFilters.search`, reset page to 1, `loadAll()` |
| `change` | `#page-size-select` | Update `currentFilters.page_size`, reset page to 1, `loadAll()` |
| `click` | `#prev-page-btn` | `currentFilters.page--`, `loadAll()` |
| `click` | `#next-page-btn` | `currentFilters.page++`, `loadAll()` |
| `show.bs.modal` | `#create-modal` | Reset form, clear errors, reset job title dropdown and salary invalid state, re-enable submit |
| `submit` | `#create-form` | Disable submit, `createEmployee()`, on success close modal + toast + `loadAll()`; on error show all errors in `#create-error`; re-enable submit in `finally` |
| `submit` | `#edit-form` | Disable submit, `updateEmployee()`, on success close modal + toast + `loadAll()`; on error show all errors in `#edit-error`; re-enable submit in `finally` |
| `click` | `#deactivate-btn` | Show `#deactivate-modal` |
| `show.bs.modal` | `#deactivate-modal` | Add `modal-dimmed` class to `#edit-modal` |
| `hidden.bs.modal` | `#deactivate-modal` | Remove `modal-dimmed`, clear `#deactivate-error` |
| `click` | `#confirm-deactivate-btn` | Disable button, `updateEmployee(id, { is_active: false })`, on success close both modals + toast + `loadAll()`; on error show in `#deactivate-error`; re-enable in `finally` |
| `click` | `#employee-tbody` (delegated, `async`) | Find closest `.edit-btn`; disable it; call `fetchEmployee(btn.dataset.id)` for fresh data; prefill edit form from `body.data`; open `#edit-modal`; re-enable button in `finally`; on error show toast |
| `change` | `.modal-dept-select` (both modals) | Rebuild the job title dropdown for that form via `populateModalJobTitles` |

**Init on page load**: if `getAccessToken()` exists → `showApp()` + `loadAll()`; else → `showLogin()`.

---

## Verification

```bash
./run_server.sh local
# Visit http://localhost:<port>/
```

Checklist:
1. Login page appears on first load; login with valid credentials loads the dashboard
2. Invalid credentials shows all errors from `error_list`
3. Salary insights cards show aggregated values; filters update both table and insights simultaneously
4. Employee table loads paginated; rows-per-page selector works
5. Search (debounced) and department filter trigger immediate reload; salary/country require Apply
6. Salary filter cross-validation: `min > max` disables Apply and shows "Must be ≥ Min Salary"
7. Clear filters resets all inputs and reloads
8. Create modal: clearing a required field and submitting shows a backend validation error
9. Edit modal: opens with fresh data from `GET /api/v1/employee/{id}/` (not stale table snapshot)
10. Rapid double-click on Create / Save / Deactivate: only one request sent (button disabled during call)
11. Deactivate: confirmation modal appears; confirmed deactivation removes employee from table
12. Logout: POSTs refresh token to `/api/v1/logout/`, clears localStorage, returns to login page
13. Token refresh: clearing the access token in DevTools and making a request silently refreshes it
14. Expired session: returns to login with "Your session has expired." message
