# -------- Base image --------
FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH"

WORKDIR /code


# -------- Install uv (pinned version) --------
COPY --from=ghcr.io/astral-sh/uv:0.4.25 /uv /usr/local/bin/uv


# -------- Create virtual environment --------
RUN uv venv /opt/venv


# -------- Install dependencies --------
ARG ENVIRONMENT

# Copy only requirements first (for caching)
COPY requirements/ ./requirements/

RUN uv pip install \
    --python /opt/venv/bin/python \
    --no-cache \
    -r requirements/${ENVIRONMENT}.txt


# Create user
RUN addgroup --system appgroup && \
    adduser --system --ingroup appgroup appuser

# Copy only required Django code
COPY manage.py .
COPY incubyte_salary_management_backend_service/ ./incubyte_salary_management_backend_service/
COPY apps/ ./apps/
COPY server.sh .
COPY static/ ./static/
COPY templates/ ./templates/

# Fix permissions
RUN chown -R appuser:appgroup /code

# Switch user
USER appuser

# -------- Start app --------
ENTRYPOINT ["bash", "server.sh"]