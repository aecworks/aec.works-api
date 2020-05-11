#!/bin/sh

source ./scripts/console.sh

type circleci &> /dev/null
if [ $? == 0 ]; then
    warn "CircleCI already Installed"
else
    info "Installing CircleCI"
    curl -fLSs https://circle.ci/cli | bash
fi

type heroku &> /dev/null
if [ $? == 0 ]; then
    warn "Heroku already Installed"
else
    info "Installing heroku"
    curl https://cli-assets.heroku.com/install.sh | sh
fi

