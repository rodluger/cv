#!/bin/bash
# Automatically update the PDF on the pdf branch with Travis. Based on
# http://www.steveklabnik.com/automatically_update_github_pages_with_travis_example/

# Exit on errors
set -o errexit -o nounset

# Begin
echo "Committing pdf..."

# Get git hash
rev=$(git rev-parse --short HEAD)

# Create *new* git repo in html folder
cd _build
git init
git config user.name "Rodrigo Luger"
git config user.email "rodluger@gmail.com"

# We will push to the pdf branch
git remote add upstream "https://$GH_TOKEN@github.com/rodluger/cv.git"
git fetch upstream && git reset upstream/pdf

# Refresh the pdf and delete aux stuff
touch cv.pdf
rm -f cv.aux
rm -f cv.log
rm -f cv.out

# Commit and push!
git add cv.pdf
git commit -m "rebuild pdf at ${rev}"
git push -q -f upstream HEAD:pdf