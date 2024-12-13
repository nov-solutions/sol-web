.PHONY: dev prod drop-db ssh mk-mig key-pair venv logs

dev:
	docker compose -f docker-compose.yaml -f docker-compose.dev.yaml up --build

prod:
	docker compose up --build

drop-db:
	docker compose -f docker-compose.dev.yaml down
	docker volume rm sol-web_pgdata

ssh:
	ssh -i "app.pem" ubuntu@EC2IPADDRESS

mk-mig:
	sudo rm ./django/*.log*
	cd django && python manage.py makemigrations
	docker exec -it sol-web-django python manage.py migrate

key-pair:
	aws ec2 create-key-pair --key-name sol-web --query 'KeyMaterial' --output text > app.pem

venv:
	python -m venv .venv
	source .venv/bin/activate
	pip install -r requirements.txt

apply:
	kubectl apply -k k8s/overlays/dev

init-secret:
	kubectl create secret generic sol-web-secret --from-env-file=.env

logs:
	kubectl logs -l app=web --all-containers=true

restart:
	kubectl rollout restart deployment sol-web

start-cluster:
	echo "Starting Minikube..."
	minikube start --cpus=4 --memory=8192
	echo "Configuring Docker to use Minikube's Docker daemon..."
	eval $$(minikube -p minikube docker-env)
	kubectl config set-context --current --namespace=dev
	echo "Building local Docker images..."
	docker build -t sol-web-django:dev ./django
	docker build -t sol-web-nextjs:dev ./nextjs
	docker build -t sol-web-nginx:dev .
	docker build -t sol-web-tailwind-watcher:dev -f ./nextjs/Dockerfile.tailwind-watcher ./nextjs
	echo "Applying the development configuration using Kustomize..."
	kubectl apply -k k8s/overlays/dev
	@echo "Mounting local directories into Minikube..."
	nohup minikube mount ./django:/mnt/django &
	nohup minikube mount ./nextjs/src:/mnt/nextjs/src &
	nohup minikube mount ./nextjs/public:/mnt/nextjs/public &
