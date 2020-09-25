#!/bin/bash

source ./scripts/console.sh

# $PORT can be set by Heroku
PORT=${PORT:-8000}

info ">>> Running collecstatic"
python3 manage.py collectstatic --noinput

info ">>> Running Migrations"
python3 manage.py migrate --noinput
# python manage.py createcachetable

info ">>> Starting Gunicorn"
exec gunicorn api.aecworks.wsgi \
    --name gunicorn \
    --bind 0.0.0.0:$PORT \
    --log-level=info \
    --log-file=- \
    "$@"
