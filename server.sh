#!/bin/bash

set -e

export DJANGO_SETTINGS_MODULE=incubyte_salary_management_backend_service.settings

BIND_ADDRESS=${SERVER_HOST}:${SERVER_PORT}

if [ "$ENVIRONMENT" = "local" ]; then
    echo "Running local development server on ${BIND_ADDRESS}"
    exec python manage.py runserver "$BIND_ADDRESS"
else
    echo "Collecting static files..."
    python manage.py collectstatic --noinput

    echo "Running gunicorn server on ${BIND_ADDRESS}"
    exec gunicorn incubyte_salary_management_backend_service.wsgi:application \
        --name incubyte_salary_management_backend_service \
        --bind "$BIND_ADDRESS" \
        --reload \
        --workers 2 \
        --log-level=debug \
        "$@"
fi