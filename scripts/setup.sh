#!/bin/sh

source ./scripts/console.sh


info "installing githooks"
git config core.hooksPath "./scripts/githooks"
