#!/bin/bash

source ./scripts/console.sh

info "Linting... 👀"

result=0
trap 'result=1' ERR
./.venv/bin/flake8 .
./.venv/bin/black . --exclude "\.venv|migrations" --diff
exit "$result"
