# Frontend + Backend Gaps — Salary Management App

Findings from a review of all API endpoints, `static/app.js`, and `templates/index.html`.
All issues have been identified and resolved.

---

## 1. SECURITY — Missing Logout / Token Blacklist Endpoint ✅

**Severity:** High

**Problem:**
The backend had `rest_framework_simplejwt`'s blacklist app installed but no `POST /api/v1/logout/` endpoint exposed. The frontend `logout()` only cleared localStorage — tokens remained valid server-side until expiry.

**Resolution:**
- **Backend:** Registered `TokenBlacklistView` at `POST /api/v1/logout/` in `apps/user/urls.py`. Added `LOGOUT_URL` and `LOGOUT_NAME` constants to `apps/user/constants.py`. Tests written first (TDD) in `apps/user/tests/api/test_logout_api.py`.
- **Frontend:** `logout()` in `app.js` made `async`; POSTs the refresh token to `/api/v1/logout/` before clearing localStorage. Call is best-effort — local logout always completes even if the server call fails.

---

## 2. BUG — Double-Submit on Create, Edit, and Deactivate ✅

**Severity:** High (data integrity)

**Problem:**
None of the submit/confirm buttons were disabled during their async API calls. Double-clicking Create could produce two duplicate employees; double-clicking Deactivate would show a confusing 404 error on the second request.

**Resolution:**
Each of the three async handlers in `app.js` now disables its button before the `await` and re-enables it in a `finally` block, covering both success and error paths:
- Create form submit button
- Edit form save button
- Deactivate confirmation button

---

## 3. UX BUG — Salary Min/Max Cross-Validation Missing ✅

**Severity:** Medium

**Problem:**
Each salary filter input was validated individually (must be 10,000–1,000,000), but there was no check that `salary_min ≤ salary_max`. Entering `min=900000, max=10000` and clicking Apply would silently return 0 results with no explanation.

**Resolution:**
`updateApplyBtn()` in `app.js` now owns all salary filter validation. After individual range checks, it cross-validates: if both fields are filled, individually valid, but `min > max`, the max field is marked invalid with the feedback text "Must be ≥ Min Salary". The Apply button stays disabled until the condition is resolved. The feedback text is reset on every evaluation and on `resetFilters()`.

---

## 4. UX GAP — Edit Modal Showed Stale Employee Data ✅

**Severity:** Medium

**Problem:**
The Edit button embedded a full JSON snapshot of the employee in a `data-employee` attribute at table-render time. If the employee was updated elsewhere between the last table load and opening the modal, the form showed outdated data. The `GET /api/v1/employee/{id}/` retrieve endpoint existed but was never used by the frontend.

**Resolution:**
Added a `fetchEmployee(id)` helper to `app.js` that calls `GET /api/v1/employee/{id}/`. The edit button click handler (now `async`) disables the button, fetches fresh data, pre-fills the form from the API response, then opens the modal. On fetch error a toast is shown. The stale `data-employee` attribute is no longer used.

**Note:** A bug introduced during this change (`await` inside a non-`async` callback) caused the entire `app.js` to fail to parse, breaking login. Fixed by adding `async` to the tbody click handler.

---

## 5. MINOR — Only First Error from `error_list` Shown ✅

**Severity:** Low

**Problem:**
`showModalError()` and the login error handler always displayed only the first entry from `error_list`. When the backend returned multiple validation errors, subsequent errors were invisible.

**Resolution:**
Added a `normalizeError(err)` helper that converts object-type errors to strings. `showModalError()` now renders a single string for one error or a `<ul>` list (using `escapeHtml` for safety) for multiple errors. The login error handler joins all errors with a space into the single-line alert.

---

## Bonus Fix — Cleared Fields Silently Ignored on Edit ✅

**Severity:** Medium (discovered during testing)

**Problem:**
`getFormData()` filtered out empty-string values (`if (value !== '') data[key] = value`). Clearing a required field like `name` in the edit modal and saving would omit that field from the PATCH payload entirely. The backend kept the old value with no error, making it look like the edit applied but the field "came back".

**Resolution:**
Removed the empty-string filter from `getFormData()`. All form fields are now included in the payload regardless of value, so clearing a required field correctly triggers a backend validation error shown in the modal.

---

## Summary Table

| # | Issue | Severity | Status |
|---|---|---|---|
| 1 | No logout/token-blacklist endpoint | High | ✅ Done |
| 2 | Double-submit on Create/Edit/Deactivate | High | ✅ Done |
| 3 | Salary min > max gives silent empty result | Medium | ✅ Done |
| 4 | Edit modal used stale table-row data | Medium | ✅ Done |
| 5 | Only first validation error displayed | Low | ✅ Done |
| — | Cleared fields silently ignored on edit | Medium | ✅ Done |
