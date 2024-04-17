tailwindcss -i input.css -o ./nextjs/public/static/css/styles.css --minify

rsync -r --delete --progress --exclude="node_modules" --exclude="nextjs/.next" --exclude="nextjs/node_modules" --exclude=".venv" --exclude=".git" --exclude="staticfiles" -e "ssh -i NEWSOLWEBAPP-web.pem" . ubuntu@TODOipaddress:app
