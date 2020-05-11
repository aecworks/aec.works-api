#!/bin/bash
source ./scripts/console.sh

# $PORT will be set by Heroku
PORT=${PORT:-5000}

info ">>> Running collecstatic"
python3 manage.py collectstatic --noinput

info ">>> Running Migrations"
python3 manage.py migrate --noinput
python manage.py createcachetable

info ">>> Starting Gunicorn"
exec gunicorn api.aecguide.wsgi \
    --name gunicorn \
    --bind 0.0.0.0:$PORT \
    --log-level=info \
    --log-file - \
    "$@"
# --workers 2 \
