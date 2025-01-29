.PHONY: dev prod drop-db ssh init-mig mk-mig key-pair venv

dev:
	docker compose -f docker-compose.yaml -f docker-compose.dev.yaml up --build

prod:
	docker compose up --build

drop-db:
	docker compose -f docker-compose.dev.yaml down
	docker volume rm newsolwebapp-web_pgdata

ssh:
	ssh -i "app.pem" ubuntu@52.38.15.163

init-mig:
	cd web && python manage.py makemigrations user
	cd web && python manage.py makemigrations admin

mk-mig:
	sudo rm ./web/*.log*
	cd web && python manage.py makemigrations
	docker exec -it newsolwebapp-web-django python manage.py migrate

key-pair:
	aws ec2 create-key-pair --key-name newsolwebapp-web --query 'KeyMaterial' --output text > app.pem

venv:
	python -m venv .venv
	source .venv/bin/activate
	pip install -r requirements.txt
