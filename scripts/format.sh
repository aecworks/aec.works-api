#!/bin/bash

source ./scripts/console.sh

black . --exclude "\.venv|migrations"
