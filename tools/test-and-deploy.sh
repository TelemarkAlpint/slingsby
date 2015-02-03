#!/bin/bash

# This script is executed by Travis to test and deploy the application

# Fail the script if any statements fail
set -e

# Lint the code, but don't fail the build if there's errors
grunt lint --force

# Unit tests
RUN_SSH_TESTS=1 FILESERVER=travis@127.0.0.1 coverage run --source slingsby ./manage.py test

# Generate HTML coverage report
coverage html -d cover

# Build
grunt build

# Perform these steps here in the 'script' section of .travis.yml to make sure that if they
# fail they'll fail the build:

./tools/coverage_to_gh_pages.sh

# Decrypt secrets needed to deploy, provision the server to make sure it's up to date, and deploy
if [[ $TRAVIS_BRANCH == 'master' ]] && [[ $TRAVIS_PULL_REQUEST == 'false' ]]; then python ./tools/secure_data.py decrypt --key $SALT_SECRET && fab provision deploy -H travis@ntnuita.no:3271; fi

# Add code coverage to gh-pages
if [[ $TRAVIS_BRANCH == 'master' ]] && [[ $TRAVIS_PULL_REQUEST == 'false' ]]; then ./tools/coverage_to_gh_pages.sh; fi
