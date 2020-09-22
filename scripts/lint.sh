#!/bin/bash

set -e
source ./scripts/console.sh

info "Linting... 👀"

./.venv/bin/flake8 .
./.venv/bin/black . --exclude "\.venv|migrations" --diff --check

info 'done'
