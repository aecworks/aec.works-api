#!/bin/bash

set -e
source ./scripts/console.sh

info "Seeding DB 🌿"

info "Seeding Companies, Comments, Profiles"
./.venv/bin/python3.8 manage.py seed

info "Creating Groups"
./.venv/bin/python3.8 manage.py groups

info "Loading Dev User"
./.venv/bin/python3.8 manage.py loaddata api/aecworks/fixtures/users.json
