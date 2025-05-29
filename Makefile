.PHONY: dev prod drop-db ssh init-mig mk-mig key-pair deploy-cdk venv

dev:
	mkdir -p ./web/static
	docker compose -f docker-compose.yaml -f docker-compose.dev.yaml up --build

test:
	docker exec -it newsolwebapp-web-django python manage.py test

prod:
	docker compose up --build

drop-db:
	docker compose -f docker-compose.yaml -f docker-compose.dev.yaml down
	docker volume rm newsolwebapp-web_pgdata

ssh:
	ssh -i "app.pem" ubuntu@IP_ADDRESS

init-mig:
	cd django && python manage.py makemigrations user
	cd django && python manage.py makemigrations admin
	docker exec -it newsolwebapp-web-django python manage.py migrate

mk-mig:
	sudo rm ./web/*.log*
	cd django && python manage.py makemigrations
	docker exec -it newsolwebapp-web-django python manage.py migrate

key-pair:
	aws ec2 create-key-pair --key-name newsolwebapp-web --query 'KeyMaterial' --output text > app.pem

deploy-cdk:
	cd cdk && cdk deploy --profile grav --outputs-file outputs.json

venv:
	python -m venv .venv
	source .venv/bin/activate
	pip install -r requirements.txt
