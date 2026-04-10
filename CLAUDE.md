# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Local Development

All development runs through Docker Compose. Never invoke `python` or `manage.py` directly — use `docker exec` into the running container instead.

### Starting the stack

```bash
./run_server.sh local        # tears down, rebuilds, and starts local environment
./run_server.sh dev          # dev environment
./run_server.sh test         # test environment
```

The `server` container is named `incubyte_salary_management_backend_service_api`. The `postgres` container is `incubyte_salary_management_backend_service_postgres`.

### Running commands inside the container

```bash
# Run all tests
docker exec incubyte_salary_management_backend_service_api pytest

# Run a single test file
docker exec incubyte_salary_management_backend_service_api pytest apps/user/tests/api/test_login_api.py

# Run tests matching a name pattern
docker exec incubyte_salary_management_backend_service_api pytest -k "test_login"

# Apply migrations
docker exec incubyte_salary_management_backend_service_api python manage.py migrate

# Create migrations for an app
docker exec incubyte_salary_management_backend_service_api python manage.py makemigrations <appname>

# Open a Django shell
docker exec -it incubyte_salary_management_backend_service_api python manage.py shell
```

### Environment files

Configuration is loaded from `.envs/<environment>/api.env` and `.envs/<environment>/db.env`. The local environment uses `.envs/local/`. RSA keys for JWT signing live in `.encryption_keys/jwt` (private) and `.encryption_keys/jwt.pub` (public).

## Domain

### Goal
Salary management tool for an organisation with 10,000 employees. Target user: **HR Manager**.

### Employee model

| Field | Type | Notes |
|-------|------|-------|
| `id` | int PK, auto | |
| `employee_id` | varchar(13) | unique; auto-generated as `EMP<n>` on create |
| `name` | varchar(300) | not null |
| `email` | varchar | unique; auto-generated as `emp_<n>@incubyte.com` on create |
| `job_title` | varchar (choices) | `JobTitle` TextChoices enum |
| `department` | varchar (choices) | `Department` TextChoices enum; must match `job_title` via `JOB_TITLE_DEPARTMENT_MAP` |
| `salary` | PositiveIntegerField | min: 10,000 / max: 1,000,000,000 |
| `joining_date` | date | not null |
| `country` | varchar (choices) | `Country` TextChoices enum |
| `is_active` | boolean | soft-delete flag (from `IsActive` mixin); default True |

`employee_id` and `email` are read-only — auto-assigned by `EmployeeCreateSerializer.create()` using `Employee.get_max_employee_number()`.

The `User` table is the standard Django auth `User` (already in `apps/user/`). `Employee` is a separate model with no FK to `User`.

### Features implemented
1. **Employee CRUD** — `POST /api/v1/employee/`, `GET /api/v1/employee/`, `GET /api/v1/employee/<pk>/`, `PATCH /api/v1/employee/<pk>/`. No hard-delete; soft-delete via `is_active=False`.
2. **Salary insights** — `GET /api/v1/employee/salary-insights/` returns `min_salary`, `max_salary`, `avg_salary` (rounded), `total_employees`. Supports all employee filters.
3. **Seed script** — `python manage.py seed_employees` bulk-creates 10,000 employees using `bulk_create` (batch size 500). Safe to run repeatedly — picks up from the current max employee number. Reads names from `apps/employee/data/first_names.txt` and `last_names.txt`.
4. **Generate name files** — `python manage.py generate_name_files` creates the name text files using Faker (`en_IN` locale).

## Architecture

### App layout

Django apps live under `apps/`. Every domain app follows a base 5-file pattern, with optional extras:

| File | Purpose |
|------|---------|
| `constants.py` | App name, URL slugs, model field constants |
| `models.py` | Django models (inherit from core mixins) |
| `serializers.py` | DRF ModelSerializers |
| `views.py` | Viewsets inheriting from `BaseViewset` |
| `urls.py` | `DefaultRouter` registration |
| `filters.py` _(optional)_ | `django-filters` FilterSet classes |
| `management/commands/` _(optional)_ | Custom management commands |

### Core abstractions (`apps/core/`)

**Base models** (`models.py`) — abstract mixins to compose into domain models:
- `Timestamps` — `created_ts` (auto_now_add), `modified_ts` (auto_now)
- `CreatedBy` / `ModifiedBy` — nullable FKs to User, SET_NULL on delete
- `IsActive` — boolean soft-delete flag

**`BaseViewset`** (`views.py`) — all 5 CRUD operations with JWT auth, pagination, and response wrapping baked in. Set `http_method_names`, `serializer_class`, `queryset`, and optionally `ordering` to get a fully working endpoint.

**Standardized response envelope** — every response (success and error) uses:
```json
{ "data": ..., "message": "...", "error_list": [...] }
```
This is enforced by `custom_exception_handlers.py` (registered as `EXCEPTION_HANDLER` in DRF settings) and `get_response()` in viewset mixins.

**Pagination** (`pagination.py`) — `ListPagination` only paginates when `?page=` is present in the request; omitting it returns all results. Page size default: 25, max: 200.

### Authentication

- Custom `User` model (`apps/user/`) uses `email` as `USERNAME_FIELD`; no `username` field.
- JWT tokens with RS256 (asymmetric RSA signing via `djangorestframework-simplejwt[crypto]`).
- Token blacklist is enabled with `BLACKLIST_AFTER_ROTATION = True`.
- Token endpoints: `POST /api/v1/login/` and `POST /api/v1/token-refresh/`.
- All non-auth endpoints require `IsAuthenticated` by default (set in `REST_FRAMEWORK` settings).

### Settings structure

Main `settings.py` imports from `incubyte_salary_management_backend_service/configurations/`:

| File | Governs |
|------|---------|
| `common_settings.py` | Installed apps, middleware, CORS, static files |
| `database_settings.py` | PostgreSQL connection |
| `jwt_settings.py` | JWT lifetimes, RS256 keys |
| `rest_framework_settings.py` | DRF defaults, exception handler, schema |
| `logger_settings.py` | Log level (from `LOG_LEVEL` env var) |
| `spectacular_settings.py` | OpenAPI title/version |
| `env_helpers.py` | `get_env_var`, `get_bool_env_var`, `get_int_env_var`, `get_list_env_var`, `get_float_env_var` |

### URL routing

All API routes are versioned under `api/v1/` (`V1_API_PREFIX` constant). Each app's `urls.py` uses `DefaultRouter` and is included in the root `incubyte_salary_management_backend_service/urls.py`. Admin (`/admin/`) and Swagger (`/api/v1/docs/`) are conditionally enabled via `ENABLE_DJANGO_ADMIN` and `ENABLE_SWAGGER` feature flags.

### Utilities in `apps/core/`

- `api_client.py` — `APIClient` for outbound HTTP calls with retry logic (max 3 retries, 10s timeout)
- `url_builder.py` — `build_url()` using `yarl` for safe URL + query param construction
- `filters.py` — `NumberInFilter` for `?field__in=1,2,3` style filtering
- `logger_mixin.py` — `LoggingMixin` for request/response logging in viewsets
- `utils.py` — `send_message_to_teams()` posts Adaptive Cards to a Teams webhook (gated by `ENABLE_TEAMS_NOTIFICATIONS`)

### Employee app specifics

**Filtering** (`EmployeeFilter`): exact match on `job_title`, `department`, `country`; range filter on `salary` via `?salary_min=` and `?salary_max=`.

**Search** (`SearchFilter`): `?search=` matches against `employee_id`, `name`, `email`.

**Serializers**: `EmployeeCreateSerializer` (auto-assigns `employee_id` + `email`, `is_active` read-only) and `EmployeeUpdateSerializer` (allows updating all editable fields). Both validate `department` matches `job_title` via `JOB_TITLE_DEPARTMENT_MAP`.

**Salary insights**: custom `@action` at `GET /api/v1/employee/salary-insights/`. Runs `aggregate()` over the filtered queryset. URL name: `employee-salary-insights`.

**Management commands**:
```bash
# Seed 10,000 employees (idempotent — picks up from max employee number)
docker exec incubyte_salary_management_backend_service_api python manage.py seed_employees

# Regenerate name source files (first_names.txt / last_names.txt)
docker exec incubyte_salary_management_backend_service_api python manage.py generate_name_files
```

### Testing

Pytest with `pytest-django`; config in `pytest.ini` (`testpaths = tests apps`).

#### Directory structure for a new app

```
apps/<app>/tests/
├── __init__.py
├── conftest.py        # app-level fixtures (URLs, payloads, model fixtures)
├── constants.py       # app-specific test strings/values
├── factories.py       # keyword-only factory functions for model creation
├── helpers.py         # domain-specific assertion helpers (optional)
└── api/
    ├── __init__.py
    └── test_<feature>_api.py
```

Global utilities live in `tests/`:
- `conftest.py` — `api_client` fixture (DRF `APIClient`)
- `constants.py` — `TEST_USER_EMAIL`, `TEST_USER_PASSWORD`, `JSON_FORMAT`
- `factories/user.py` — `create_user(*, email, password)` keyword-only factory
- `helpers/assertions.py` — `assert_error_response(response, expected_status_code)`

#### Conventions to follow exactly

**Mark every test module for DB access at the top:**
```python
pytestmark = pytest.mark.django_db
```

**Test classes** are named `Test<Resource><Action>` (e.g., `TestLoginApi`, `TestTagApi`).

**Test method names** are fully descriptive sentences:
```python
def test_returns_access_and_refresh_tokens_for_valid_credentials(...)
def test_returns_unauthorized_for_invalid_credentials(...)
def test_returns_bad_request_when_password_is_missing(...)
```

**All constants go in `constants.py`** — never hardcode strings, field names, or token keys inline in test files.

**URL fixtures use `reverse()`** with the URL name constant — never hardcode URL strings:
```python
@pytest.fixture
def login_url():
    return reverse(LOGIN_NAME)
```

**Factory functions use keyword-only args** with defaults from the app's own `tests/constants.py` (or global `tests/constants.py` for the `User` factory):
```python
def create_user(*, email=TEST_USER_EMAIL, password=TEST_USER_PASSWORD):
    return get_user_model().objects.create_user(email=email, password=password)

def create_employee(*, name=TEST_EMPLOYEE_NAME, salary=TEST_EMPLOYEE_SALARY, ...):
    return Employee.objects.create(name=name, salary=salary, ...)
```

**Always pass `format=JSON_FORMAT`** to API calls:
```python
response = api_client.post(url, payload, format=JSON_FORMAT)
```

**Happy-path assertions** check `status_code` and expected `response.data` keys directly.

**Error-path assertions** use `assert_error_response()`, which verifies the envelope shape (`data` is None, `message` is None, `error_list` is non-empty):
```python
assert_error_response(response, status.HTTP_401_UNAUTHORIZED)
```

**Field-level error assertions** iterate `error_list`:
```python
assert any(PASSWORD_FIELD in error for error in response.data["error_list"])
```

### Adding a new CRUD resource

Use the `/drf-crud` skill or follow the `Employee` app as reference (`apps/employee/`):

1. `docker exec incubyte_salary_management_backend_service_api python manage.py startapp <appname> apps/<appname>`
2. Create `constants.py`, `models.py`, `serializers.py`, `views.py`, `urls.py`, `apps.py` following the Employee pattern.
3. Add `"apps.<appname>"` to `PROJECT_APPS` in `settings.py`.
4. Include `apps.<appname>.urls` in `incubyte_salary_management_backend_service/urls.py` under `V1_API_PREFIX`.
5. `docker exec incubyte_salary_management_backend_service_api python manage.py makemigrations <appname> && python manage.py migrate`
