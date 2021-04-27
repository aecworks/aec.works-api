#!/bin/bash

set -e
source ./scripts/console.sh

info "Seeding DB 🌿"

./.venv/bin/python3.8 manage.py seed
./.venv/bin/python3.8 manage.py groups
