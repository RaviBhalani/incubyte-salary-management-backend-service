# Incubyte Salary Management

A salary management tool for HR Managers to create, view, update, and analyse employee salary data.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Django 6.0 + Django REST Framework |
| Auth | JWT (RS256) via `djangorestframework-simplejwt` |
| Database | PostgreSQL (`psycopg`) |
| Static files | WhiteNoise (non-local) |
| Server | Gunicorn (non-local) / Django `runserver` (local) |
| Containerisation | Docker + Docker Compose |
| API docs | drf-spectacular (Swagger UI) |
| Frontend | Django Templates + plain HTML/CSS/JS (Bootstrap 5) |

---

## Project Structure

```
.
├── apps/
│   ├── core/               # Shared abstractions: base models, viewsets, pagination, utilities
│   ├── employee/           # Employee model, CRUD endpoints, salary insights, seed commands
│   └── user/               # Custom User model (email-based), login, token refresh, logout
├── incubyte_salary_management_backend_service/
│   ├── configurations/     # Modular settings files (jwt, database, logging, etc.)
│   ├── settings.py         # Main settings — imports from configurations/
│   └── urls.py             # Root URL config
├── static/                 # Frontend JS and CSS source files
│   ├── app.js
│   └── style.css
├── templates/
│   └── index.html          # Single-page app shell
├── tests/                  # Global test utilities (conftest, factories, helpers)
├── docs/
│   ├── guides/             # Implementation plans and gap analyses (markdown)
│   ├── postman/            # Postman collection and environment
│   └── ER Diagram.drawio.png
├── requirements/
│   ├── base.txt            # Shared dependencies
│   ├── local.txt           # Local overrides
│   ├── dev.txt             # Dev overrides
│   ├── test.txt            # Test overrides
│   └── prod.txt            # Prod overrides
├── .envs/
│   ├── local/              # Local environment files (api.env, db.env)
│   └── api.env             # Template for non-local environments
├── .encryption_keys/       # RSA private/public keys for JWT signing (local only)
├── Dockerfile
├── docker-compose.local.yaml
├── docker-compose.dev.yaml
├── docker-compose.test.yaml
├── docker-compose.prod.yaml
├── server.sh               # Container entrypoint (runserver / collectstatic + gunicorn)
└── run_server.sh           # Helper to tear down, rebuild, and start the stack
```

---

## Local Development Setup

### Prerequisites

- Docker and Docker Compose
- RSA key pair for JWT signing

### 1. Generate RSA keys

```bash
mkdir -p .encryption_keys
openssl genrsa -out .encryption_keys/jwt 2048
openssl rsa -in .encryption_keys/jwt -pubout -out .encryption_keys/jwt.pub
```

### 2. Configure environment files

Three env files are needed for local development:

| File | Purpose |
|------|---------|
| `.envs/local.env` | Compose-level variables (`UID`, `GID`, `SERVER_PORT`) — passed to Docker Compose via `--env-file` |
| `.envs/local/api.env` | Application settings (Django, JWT, feature flags, etc.) — loaded inside the container |
| `.envs/local/db.env` | Database credentials — loaded inside the container |

Defaults are already provided and work out of the box. Fill in any blank values before starting. See `.envs/api.env` for the full list of available application variables.

### 3. Start the stack

```bash
./run_server.sh local
```

This tears down any existing containers, rebuilds the image, runs migrations, and starts the server.

The app will be available at `http://localhost:8000`.

---

## Management Commands

All commands must be run inside the container:

```bash
docker exec incubyte_salary_management_backend_service_api <command>
```

| Command | Description |
|---------|-------------|
| `pytest` | Run the full test suite |
| `pytest apps/user/tests/api/test_login_api.py` | Run a specific test file |
| `pytest -k "test_login"` | Run tests matching a name pattern |
| `python manage.py create_superuser --email <email> --password <password> --first-name <first> --last-name <last>` | Create a superuser. Skips silently if a user with that email already exists. |
| `python manage.py seed_employees` | Bulk-create employees (idempotent — picks up from current max employee number). Safe to run repeatedly. |
| `python manage.py generate_name_files` | Regenerate `first_names.txt` and `last_names.txt` source files used by the seed command (uses Faker, `en_IN` locale) |

---

## Environment-Specific Configuration

Several settings differ between local and non-local environments:

| Setting | Local | Non-local |
|---------|-------|-----------|
| Database | Individual `POSTGRES_*` vars | `POSTGRES_URL` (parsed by `dj-database-url`) |
| RSA keys | Filenames in `.encryption_keys/` | Full PEM content in `RSA_PRIVATE_KEY` / `RSA_PUBLIC_KEY` env vars (use `\n` for newlines) |
| Static files | Served by `runserver` | Collected via `collectstatic` at startup, served by WhiteNoise |
| Web server | Django `runserver` | Gunicorn (2 workers) |

For non-local deployments, copy `.envs/api.env` as a reference and populate all required values via your platform's secret management.

---

## Frontend

A minimal single-page application served directly by Django — no Node.js, no build step.

- `templates/index.html` — app shell with login form and employee dashboard
- `static/app.js` — all API calls, auth logic, and DOM rendering
- `static/style.css` — minor Bootstrap overrides

The frontend communicates exclusively with the REST API. Static files are served by WhiteNoise in non-local environments (with content-hashed filenames and gzip/Brotli compression). In local development, Django's built-in static file serving is used.
