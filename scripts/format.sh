#!/bin/bash

source ./scripts/console.sh

info "Formatting 🧹"

./.venv/bin/black . --exclude "\.venv|migrations"
./.venv/bin/isort . --profile black
