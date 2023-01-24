#!/bin/sh

source ./scripts/console.sh


pybinary="python3.8"


$pybinary -V &> /dev/null
if [ $? -ne 0 ]; then
    # Can't find python
    error "$pybinary binary could not be found 🤷‍♀️"
    error "make sure you have python 3.8 installed and available in your PATH"
    exit 1
else
    info  "$pybinary  found - very nice ✨"

    # Delete existing env if found
    [ -d ".venv" ] && warn "deleting existing virtual enviroment" && rm -rdf .venv

    info  "creating python virtual environment 🏠"
    $pybinary -m venv .venv

    info  "installing python dependencies - hang tight 🕐"
    "./.venv/bin/$pybinary" -m pip install -q --upgrade pip
    "./.venv/bin/$pybinary" -m pip install -q -r requirements.txt
    "./.venv/bin/$pybinary" -m pip install -q -r requirements-dev.txt

    info "all done! you can use this venv later with  'source .venv/bin/activate'"
fi

info "installing githooks"
git config core.hooksPath "./scripts/githooks"
