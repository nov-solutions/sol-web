include .env

dev:
	docker compose -f docker-compose.dev.yaml up --build
prod:
	docker compose up --build

gen-certs:
	openssl genrsa -out server.key 2048
	openssl req -new -x509 -sha256 -key server.key -out server.crt -days 365

export-db:
	python manage.py dumpdata > seed.json

seed-db:
	python manage.py loaddata seed.json

drop-db-dev:
	docker compose -f docker-compose.dev.yaml down
	docker volume rm NEWSOLWEBAPP_pgdata

drop-db-prod:
	docker compose down
	docker volume rm NEWSOLWEBAPP_pgdata

key-pair:
	aws ec2 create-key-pair --key-name NEWSOLWEBAPP-web-39 --query 'KeyMaterial' --output text > NEWSOLWEBAPP-web.pem

venv:
	python -m venv .venv
	source .venv/bin/activate
	pip install -r requirements.txt
