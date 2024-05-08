cd ./nextjs

npx tailwindcss -i ./public/static/css/input.css -o ./public/static/css/styles.css --minify

cd ../

rsync -r --delete --progress --exclude="node_modules" --exclude="nextjs/.next" --exclude="nextjs/node_modules" --exclude=".venv" --exclude=".git" --exclude="staticfiles" -e "ssh -i NEWSOLWEBAPP-web.pem" . ubuntu@TODOipaddress:app
