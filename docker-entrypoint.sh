#!/usr/bin/env bash
set -euo pipefail

: "${PORT:=8000}"
: "${WEB_CONCURRENCY:=3}"
: "${MIGRATE:=1}"
: "${COLLECTSTATIC:=1}"
: "${DEV_SERVER:=0}"

if [[ "${DEV_SERVER}" != "1" ]]; then
  echo "Running Django deploy checks"
  uv run manage.py check --deploy
fi

if [[ "${MIGRATE}" == "1" ]]; then
  echo "Applying database migrations"
  uv run manage.py migrate --noinput
else
  echo "Skipping migrations (MIGRATE=${MIGRATE})"
fi

if [[ "${COLLECTSTATIC}" == "1" ]]; then
  echo "Collecting static files"
  uv run manage.py collectstatic --noinput
else
  echo "Skipping collectstatic (COLLECTSTATIC=${COLLECTSTATIC})"
fi

echo "Starting application"
if [[ "${DEV_SERVER}" == "1" ]]; then
  echo "DEV_SERVER=1 -> using runserver on 0.0.0.0:${PORT}"
  exec uv run manage.py runserver 0.0.0.0:"${PORT}"
else
  : "${WSGI_MODULE:=hello_world_api.wsgi:application}"
  echo "Using Gunicorn (${WEB_CONCURRENCY} workers) on 0.0.0.0:${PORT}"
  exec gunicorn "${WSGI_MODULE}" \
      --bind 0.0.0.0:"${PORT}" \
      --workers "${WEB_CONCURRENCY}" \
      --timeout 30 \
      --access-logfile '-' --error-logfile '-'
fi