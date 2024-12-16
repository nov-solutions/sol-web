.PHONY: dev prod drop-db ssh mk-mig key-pair venv logs

dev:
	docker compose -f docker-compose.yaml -f docker-compose.dev.yaml up --build

prod:
	docker compose up --build

drop-db:
	docker compose -f docker-compose.dev.yaml down
	docker volume rm newsolwebapp-web_pgdata

ssh:
	ssh -i "app.pem" ubuntu@EC2IPADDRESS

mk-mig:
	sudo rm ./django/*.log*
	cd django && python manage.py makemigrations
	docker exec -it newsolwebapp-web-django python manage.py migrate

key-pair:
	aws ec2 create-key-pair --key-name newsolwebapp-web --query 'KeyMaterial' --output text > app.pem

venv:
	python -m venv .venv
	source .venv/bin/activate
	pip install -r requirements.txt

apply:
	kubectl apply -k k8s/overlays/dev

secret-init:
	kubectl create secret generic event-web-secret --from-env-file=.env

secret-update:
	kubectl create secret generic event-web-secret --from-env-file=.env --dry-run=client -o yaml | kubectl apply -f -

logs:
	kubectl logs -f -l app=web --all-containers=true --max-log-requests=7

restart:
	kubectl rollout restart deployment newsolwebapp-web

start-cluster:
	echo "Starting Minikube..."
	minikube start --cpus=4 --memory=8192
	echo "Configuring Docker to use Minikube's Docker daemon..."
	eval $$(minikube -p minikube docker-env)
	kubectl config set-context --current --namespace=dev
	echo "Building local Docker images..."
	docker build -t newsolwebapp-web-django:dev -f ./django/Dockerfile.django --build-arg BUILD_ENV=dev ./django
	docker build -t newsolwebapp-web-nextjs:dev -f ./nextjs/Dockerfile.nextjs --build-arg BUILD_ENV=dev ./nextjs
	docker build -t newsolwebapp-web-nginx:dev -f ./Dockerfile.nginx --build-arg BUILD_ENV=dev .
	docker build -t newsolwebapp-web-tailwind-watcher:dev -f ./nextjs/Dockerfile.tailwind-watcher ./nextjs
	echo "Applying the development configuration using Kustomize..."
	kubectl apply -k k8s/overlays/dev
	@echo "Mounting local directories into Minikube..."
	nohup minikube mount ./django:/mnt/django &
	nohup minikube mount ./nextjs/src:/mnt/nextjs/src &
	nohup minikube mount ./nextjs/public:/mnt/nextjs/public &
