#!/bin/bash

source ./scripts/console.sh

info " Running collecstatic"
python3 manage.py collectstatic --noinput

info " Checking DB Connection"
while ! python3 manage.py inspectdb >/dev/null; do
warn " DB is not ready"
sleep 2
done
info " DB is ready"

info ">>> Running Migrations"
python3 manage.py migrate --noinput
# python manage.py createcachetable

info "Starting Django Dev Server..."
exec python3 manage.py runserver 0.0.0.0:8000
