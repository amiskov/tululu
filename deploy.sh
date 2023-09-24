#!/usr/bin/env sh

# abort on errors
set -e

# build
poetry run python render_website.py

# Create and navigate into the build output directory
rm -rf public
mkdir -p public
cp -r pages public
cp -r assets public
cp -r images public
cp -r books public
cd public

git init
git add -A
git commit -m 'deploy'

# if you are deploying to https://<USERNAME>.github.io/<REPO>
git push -f git@github.com:amiskov/tululu.git master:gh-pages
cd -
rm -rf public
