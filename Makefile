.PHONY: dev prod drop-db ssh mk-mig key-pair venv

dev:
	docker compose -f docker-compose.yaml -f docker-compose.dev.yaml up --build

prod:
	docker compose up --build

drop-db:
	docker compose -f docker-compose.dev.yaml down
	docker volume rm app_pgdata

ssh:
	ssh -i "app.pem" ubuntu@EC2IPADDRESS

mk-mig:
	sudo rm ./django/*.log*
	cd django && python manage.py makemigrations
	docker exec -it app-django python manage.py migrate

key-pair:
	aws ec2 create-key-pair --key-name app --query 'KeyMaterial' --output text > app.pem

venv:
	python -m venv .venv
	source .venv/bin/activate
	pip install -r requirements.txt
