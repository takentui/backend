#!/usr/bin/env bash

VARIABLE_NAME=${VARIABLE_NAME:-app}

export PYTHONPATH=$PYTHONPATH:/appuser

HOST=${HOST:-0.0.0.0}
PORT=${PORT:-8000}
LOG_LEVEL=${LOG_LEVEL:-info}

case "$1" in
  "makemigrations")
    echo "Running django..."
    python manage.py makemigrations
    ;;
  "migrate-then-start")
    echo "Running django..."
    python manage.py migrate
    python manage.py runserver ${HOST}:${PORT}
    ;;
  "start")
    echo "Running django..."
    python manage.py runserver ${HOST}:${PORT}
    ;;
  "test")
    echo "Running django..."
    python manage.py test
    ;;
  *)
    exec ${@}
    ;;
esac
