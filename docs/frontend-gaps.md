# Frontend + Backend Gaps — Salary Management App

Findings from a review of all API endpoints, `static/app.js`, and `templates/index.html`.
Issues are ordered by severity.

---

## 1. SECURITY — Missing Logout / Token Blacklist Endpoint

**Severity:** High

**What's missing:**
The backend has `rest_framework_simplejwt`'s blacklist app installed and `BLACKLIST_AFTER_ROTATION = True` in `jwt_settings.py`, but there is no `POST /api/v1/logout/` endpoint. The frontend `logout()` function (`app.js:82–87`) only calls `clearTokens()` and `showLogin()` — it never tells the server.

**Impact:** After logout, the access token remains valid server-side until it expires. Anyone who captures the token (shared machine, browser history, logs) can keep calling the API after the user has "logged out."

**Fix:**
- **Backend:** Add `TokenBlacklistView` (from `rest_framework_simplejwt.views`) at `POST /api/v1/logout/`. It accepts `{"refresh": "<token>"}` and blacklists the refresh token.
- **Frontend:** Before clearing localStorage in `logout()`, POST the refresh token to the new logout endpoint.

Files to change:
- `apps/user/urls.py` — add path
- `apps/user/constants.py` — add `LOGOUT_URL`, `LOGOUT_NAME`
- `static/app.js` — update `logout()` and `ENDPOINTS`

---

## 2. BUG — Double-Submit on Create, Edit, and Deactivate

**Severity:** High (data integrity)

**What's missing:**
None of the submit/confirm buttons are disabled during their async API call.

| Handler | Location | Risk |
|---|---|---|
| Create form submit | `app.js:565–573` | Two clicks → two duplicate employees created |
| Edit form submit | `app.js:577–587` | Two clicks → two PATCH requests |
| Confirm deactivate button | `app.js:603–613` | Second request gets 404 (already deactivated); shows confusing error |

**Fix:** Disable the button at request start, re-enable in a `finally` block.

Files to change:
- `static/app.js` — three async submit handlers

---

## 3. UX BUG — Salary Min/Max Cross-Validation Missing

**Severity:** Medium

**What's missing:**
The filter panel validates each salary input individually (must be 10,000–1,000,000 via `validateSalaryInput()`), but there is **no check that `salary_min ≤ salary_max`**. A user can enter `min=900000, max=10000`, click Apply, and the API silently returns 0 results. The table shows "No employees found." with no explanation.

**Fix:** In `updateApplyBtn()` (`app.js:485–489`), add a cross-field check: if both inputs are non-empty and `min > max`, mark one input as invalid and keep the Apply button disabled. Add a corresponding `invalid-feedback` message ("Min must be ≤ Max").

Files to change:
- `static/app.js` — `updateApplyBtn()`
- `templates/index.html` — add `invalid-feedback` div for cross-validation message

---

## 4. UX GAP — Edit Modal Shows Stale Employee Data

**Severity:** Medium

**What's missing:**
Clicking the Edit button reads employee data from the `data-employee` attribute on the button (`app.js:616–630`) — a JSON snapshot embedded at table-render time. If the employee was updated (in another tab, or right after loading) since the table last refreshed, the form shows outdated values.

The `GET /api/v1/employee/{id}/` (retrieve) endpoint exists but is never called by the frontend.

**Fix:** In the edit-button click handler, call a new `fetchEmployee(id)` helper that hits `GET /api/v1/employee/{id}/` before opening the modal. Show a brief loading indicator while fetching.

Files to change:
- `static/app.js` — edit button click handler; add `fetchEmployee(id)` helper

---

## 6. MINOR — Only First Error from `error_list` Shown

**Severity:** Low

**What's missing:**
`showModalError()` (`app.js:420–425`) and the login error handler (`app.js:68–69`) always display only `errorList?.[0]`. When the backend returns multiple validation errors (e.g., invalid salary AND mismatched department/job_title), only the first is visible. The user must fix one error at a time without knowing there are more.

**Fix:** Join all errors into a single message or render them as a `<ul>` list inside the alert.

Files to change:
- `static/app.js` — `showModalError()` and login error block

---

## Summary Table

| # | Issue | Severity | Backend change? | Frontend change? |
|---|---|---|---|---|
| 1 | No logout/token-blacklist endpoint | High | Yes | Yes |
| 2 | Double-submit on Create/Edit/Deactivate | High | No | Yes |
| 3 | Salary min > max gives silent empty result | Medium | No | Yes |
| 4 | Edit modal uses stale table-row data | Medium | No | Yes |
| 5 | Only first validation error displayed | Low | No | Yes |
