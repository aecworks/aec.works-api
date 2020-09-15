#!/bin/bash

source ./scripts/console.sh

info "Running Test Suite 💪"

./.venv/bin/python3.8 -m pytest
exit $?
