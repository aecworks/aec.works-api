#!/bin/bash

source ./scripts/console.sh

info "Linting..."
flake8 .
