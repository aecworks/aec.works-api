#!/bin/bash

source ./scripts/console.sh

info "Cleanning up files 🧻"

./.venv/bin/python3.8 -c "import pathlib; [p.unlink() for p in pathlib.Path('.').rglob('*.py[co]')]"
./.venv/bin/python3.8 -c "import pathlib; [p.rmdir() for p in pathlib.Path('.').rglob('__pycache__')]"
