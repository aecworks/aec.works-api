#!/bin/bash

set -e
source ./scripts/console.sh

info "Linting... 👀"

info "Flake8"
./.venv/bin/flake8 .
info "Black"
./.venv/bin/black . --exclude "\.venv|migrations" --diff --check
info "Isort"
./.venv/bin/isort . --profile black --diff

info 'done'
