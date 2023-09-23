#!/usr/bin/env sh

# abort on errors
set -e

# build
poetry run python render_website.py

# navigate into the build output directory
cd pages

# mkdir -p public
# cp pages/*.html public
# cp -r assets public



# if you are deploying to a custom domain
# echo 'oggetto.academy' > CNAME

git init
git add -A
git commit -m 'deploy'

# if you are deploying to https://<USERNAME>.github.io/<REPO>
git push -f git@github.com:amiskov/tululu.git master:gh-pages
cd -
