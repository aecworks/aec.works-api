#!/bin/sh

source ./scripts/console.sh

info "fetching shared .env file from github.com/aecworks/aecworks-env"
git clone -q --depth=1 https://github.com/aecworks/aecworks-env
mv aecworks-env/.env ./.env
rm -rdf aecworks-env

info ".env updated"
