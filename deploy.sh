#!/bin/bash
# Automatically update the PDF on the pdf branch with Travis. Based on
# http://www.steveklabnik.com/automatically_update_github_pages_with_travis_example/
# and
# https://github.com/dfm/imprs/blob/master/.travis.yml#L50

# Exit on errors
set -o errexit -o nounset

# Begin
echo "Committing pdf..."

# Get git hash
rev=$(git rev-parse --short HEAD)

# Create orphan repo (DFM's hack)
cd $TRAVIS_BUILD_DIR
git checkout --orphan pdf
git rm -rf .
git add -f cv.pdf
git -c user.name='travis' -c user.email='travis' commit -m "rebuild pdf at ${rev}"
git push -q -f https://$GH_TOKEN@github.com/$TRAVIS_REPO_SLUG pdf