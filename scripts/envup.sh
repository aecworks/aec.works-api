#!/bin/sh

source ./scripts/console.sh

info "🔑 fetching shared .env file from github.com/aecworks/aecworks-env"
git clone -q --depth=1 https://github.com/aecworks/aecworks-env

if [ $? -eq 0 ]; then
    info "  fetched env "
    info "✏️ overriding local .env"
    mv aecworks-env/.env ./.env
    rm -rdf aecworks-env
else
    warn "🤷‍♂️ could not fetch aecworks.env/.env"
    warn "🏴‍☠️ using simple .env. Oauth and AWS Assets will be disabled"
    cp .env.sample .env
fi

info "✅ .env updated"
