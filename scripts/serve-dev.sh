#!/bin/bash

source ./scripts/console.sh

info "Activating python venv"
source .venv/bin/activate || exit 1

info "Running collecstatic"
python manage.py collectstatic --noinput --link -v 0 --no-post-process --ignore .venv

info "Checking DB Connection"
while ! python manage.py inspectdb >/dev/null; do
warn "DB is not ready"
sleep 1
done
info "DB is ready"

info ">>> Running Migrations"
python manage.py migrate --noinput
# python manage.py createcachetable

info ">>> Adding Dev User"
python manage.py loaddata api/aecworks/fixtures/users.json

info "Starting Django Dev Server..."
exec python manage.py runserver 8000
