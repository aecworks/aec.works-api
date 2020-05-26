#!/bin/bash

source ./scripts/console.sh

info "Linting..."

result=0
trap 'result=1' ERR
flake8 .
black . --exclude "\.venv|migrations" --diff
exit "$result"
