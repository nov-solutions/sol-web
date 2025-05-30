# Sol Web Helm Chart

This Helm chart deploys the Sol Web application stack on Kubernetes, including Django, Next.js, Nginx, PostgreSQL, Redis, and Celery workers.

## Prerequisites

- Kubernetes 1.19+
- Helm 3.2.0+
- PV provisioner support in the underlying infrastructure (for persistence)
- LoadBalancer support (for Nginx service) or Ingress controller

## Local Development with Minikube

### Setup Minikube

1. **Install Minikube** (if not already installed):

```bash
# Linux
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
```

2. **Start Minikube with sufficient resources**:

```bash
minikube start --cpus 4 --memory 8192 --disk-size 20g
```

3. **Enable required addons**:

```bash
minikube addons enable ingress
minikube addons enable storage-provisioner
minikube addons enable metrics-server
```

### Build and Load Docker Images

Since Minikube runs in its own Docker environment, you need to build images inside Minikube or load them:

**Option 1: Build directly in Minikube's Docker environment**:

```bash
# Point your Docker client to Minikube's Docker daemon
eval $(minikube docker-env)

# Build images
docker build -f web/Dockerfile.django -t sol-web-django:latest ./web
docker build -f nextjs/Dockerfile.nextjs -t sol-web-nextjs:latest ./nextjs
docker build -f Dockerfile.nginx -t sol-web-nginx:latest .
```

**Option 2: Build locally and load into Minikube**:

```bash
# Build images locally
docker build -f web/Dockerfile.django -t sol-web-django:latest ./web
docker build -f nextjs/Dockerfile.nextjs -t sol-web-nextjs:latest ./nextjs
docker build -f Dockerfile.nginx -t sol-web-nginx:latest .

# Load images into Minikube
minikube image load sol-web-django:latest
minikube image load sol-web-nextjs:latest
minikube image load sol-web-nginx:latest
```

### Create Minikube Values File

Create a `minikube-values.yaml` file:

```yaml
# minikube-values.yaml
global:
  environment: development
  siteDomain: sol-web.local
  siteBaseDomain: http://sol-web.local

# Use local images without pulling
django:
  image:
    repository: sol-web-django
    tag: latest
    pullPolicy: Never
  replicaCount: 1
  resources:
    limits:
      cpu: 500m
      memory: 512Mi
    requests:
      cpu: 250m
      memory: 256Mi

nextjs:
  image:
    repository: sol-web-nextjs
    tag: latest
    pullPolicy: Never
  replicaCount: 1
  resources:
    limits:
      cpu: 500m
      memory: 512Mi
    requests:
      cpu: 250m
      memory: 256Mi

nginx:
  image:
    repository: sol-web-nginx
    tag: latest
    pullPolicy: Never
  replicaCount: 1
  service:
    type: NodePort
  resources:
    limits:
      cpu: 250m
      memory: 256Mi
    requests:
      cpu: 100m
      memory: 128Mi

# Reduce resource requirements for local development
celeryWorker:
  replicaCount: 1
  resources:
    limits:
      cpu: 500m
      memory: 512Mi
    requests:
      cpu: 250m
      memory: 256Mi

celeryBeat:
  resources:
    limits:
      cpu: 250m
      memory: 256Mi
    requests:
      cpu: 100m
      memory: 128Mi

postgresql:
  primary:
    persistence:
      size: 2Gi
    resources:
      limits:
        cpu: 500m
        memory: 512Mi
      requests:
        cpu: 250m
        memory: 256Mi

redis:
  master:
    persistence:
      size: 1Gi
    resources:
      limits:
        cpu: 250m
        memory: 256Mi
      requests:
        cpu: 100m
        memory: 128Mi

# Configure ingress for local development
ingress:
  enabled: true
  className: nginx
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
  hosts:
    - host: sol-web.local
      paths:
        - path: /
          pathType: Prefix
  tls: []

# Disable persistence for local development (optional)
persistence:
  enabled: false
```

### Deploy to Minikube

1. **Add Helm dependencies**:

```bash
cd helm
helm dependency update
```

2. **Install the chart**:

```bash
helm install sol-web . -f minikube-values.yaml
```

3. **Wait for pods to be ready**:

```bash
kubectl get pods -w
```

### Access the Application

**Option 1: Using NodePort (recommended for Minikube)**:

```bash
# Get the Minikube IP and NodePort
minikube service sol-web-nginx --url

# This will output something like:
# http://192.168.49.2:30123
```

**Option 2: Using Ingress**:

```bash
# Add entry to /etc/hosts
echo "$(minikube ip) sol-web.local" | sudo tee -a /etc/hosts

# Access via browser
open http://sol-web.local
```

**Option 3: Using kubectl port-forward**:

```bash
# Forward Nginx service
kubectl port-forward service/sol-web-nginx 8080:80

# Access at http://localhost:8080
```

### Useful Minikube Commands

```bash
# View Minikube dashboard
minikube dashboard

# View logs
minikube logs

# SSH into Minikube VM
minikube ssh

# Get service URLs
minikube service list

# Clean up
helm uninstall sol-web
minikube stop
minikube delete
```

### Troubleshooting Minikube

1. **If pods are stuck in ImagePullBackOff**:

   - Ensure images are loaded: `minikube image ls | grep sol-web`
   - Check pullPolicy is set to "Never" in values

2. **If services are not accessible**:

   - Check service status: `minikube service list`
   - Try port-forwarding instead of NodePort

3. **If running out of resources**:

   - Increase Minikube resources: `minikube stop && minikube start --cpus 6 --memory 10240`
   - Reduce replicas and resource requests in values file

4. **View application logs**:

```bash
# Django logs
kubectl logs -l app.kubernetes.io/component=django -f

# All pods
kubectl logs -l app.kubernetes.io/instance=sol-web
```

## Installation

### Add Helm repository dependencies

```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
```

### Install the chart

```bash
# Install with default values
helm install sol-web ./helm

# Install with custom values
helm install sol-web ./helm -f custom-values.yaml

# Install in a specific namespace
helm install sol-web ./helm -n production --create-namespace
```

## Configuration

The following table lists the main configurable parameters of the Sol Web chart and their default values.

### Global Parameters

| Parameter               | Description      | Default            |
| ----------------------- | ---------------- | ------------------ |
| `global.environment`    | Environment name | `production`       |
| `global.siteName`       | Site name        | `sol`              |
| `global.siteBaseDomain` | Base domain URL  | `http://localhost` |
| `global.siteDomain`     | Site domain      | `localhost`        |

### Django Parameters

| Parameter                        | Description               | Default                   |
| -------------------------------- | ------------------------- | ------------------------- |
| `django.enabled`                 | Enable Django deployment  | `true`                    |
| `django.replicaCount`            | Number of Django replicas | `2`                       |
| `django.image.repository`        | Django image repository   | `sol-web-django`          |
| `django.image.tag`               | Django image tag          | `latest`                  |
| `django.resources.limits.cpu`    | CPU limit                 | `1000m`                   |
| `django.resources.limits.memory` | Memory limit              | `1Gi`                     |
| `django.secretEnv.SECRET_KEY`    | Django secret key         | `change-me-in-production` |

### Next.js Parameters

| Parameter                 | Description                | Default          |
| ------------------------- | -------------------------- | ---------------- |
| `nextjs.enabled`          | Enable Next.js deployment  | `true`           |
| `nextjs.replicaCount`     | Number of Next.js replicas | `2`              |
| `nextjs.image.repository` | Next.js image repository   | `sol-web-nextjs` |
| `nextjs.image.tag`        | Next.js image tag          | `latest`         |

### Database Parameters

| Parameter                  | Description       | Default                   |
| -------------------------- | ----------------- | ------------------------- |
| `postgresql.enabled`       | Deploy PostgreSQL | `true`                    |
| `postgresql.auth.database` | Database name     | `soldb`                   |
| `postgresql.auth.username` | Database user     | `soluser`                 |
| `postgresql.auth.password` | Database password | `change-me-in-production` |

### Redis Parameters

| Parameter             | Description    | Default                   |
| --------------------- | -------------- | ------------------------- |
| `redis.enabled`       | Deploy Redis   | `true`                    |
| `redis.auth.password` | Redis password | `change-me-in-production` |

### Ingress Parameters

| Parameter                   | Description     | Default       |
| --------------------------- | --------------- | ------------- |
| `ingress.enabled`           | Enable ingress  | `true`        |
| `ingress.className`         | Ingress class   | `nginx`       |
| `ingress.hosts[0].host`     | Hostname        | `example.com` |
| `ingress.tls[0].secretName` | TLS secret name | `sol-web-tls` |

## Custom Values Examples

### Production deployment with external database

```yaml
# production-values.yaml
global:
  environment: production
  siteDomain: myapp.com
  siteBaseDomain: https://myapp.com

django:
  replicaCount: 3
  secretEnv:
    SECRET_KEY: "your-production-secret-key"
    SENTRY_DSN: "your-sentry-dsn"
    STRIPE_SECRET_KEY: "your-stripe-secret"

postgresql:
  enabled: false
  externalHost: "external-postgres.example.com"

ingress:
  hosts:
    - host: sol.grav.solutions
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: sol-web-tls
      hosts:
        - sol.grav.solutions
```

### Development deployment

```yaml
# dev-values.yaml
global:
  environment: development

django:
  replicaCount: 1
  resources:
    limits:
      cpu: 500m
      memory: 512Mi

nextjs:
  replicaCount: 1

postgresql:
  primary:
    persistence:
      size: 1Gi

redis:
  master:
    persistence:
      size: 1Gi

ingress:
  enabled: false

nginx:
  service:
    type: NodePort
```

## Building Docker Images

Before deploying, build and push your Docker images:

```bash
# Build Django image
docker build -f web/Dockerfile.django -t your-registry/sol-web-django:latest ./web
docker push your-registry/sol-web-django:latest

# Build Next.js image
docker build -f nextjs/Dockerfile.nextjs -t your-registry/sol-web-nextjs:latest ./nextjs
docker push your-registry/sol-web-nextjs:latest

# Build Nginx image
docker build -f Dockerfile.nginx -t your-registry/sol-web-nginx:latest .
docker push your-registry/sol-web-nginx:latest
```

Update your values file with the correct image repositories:

```yaml
django:
  image:
    repository: your-registry/sol-web-django
    tag: latest

nextjs:
  image:
    repository: your-registry/sol-web-nextjs
    tag: latest

nginx:
  image:
    repository: your-registry/sol-web-nginx
    tag: latest
```

## Persistence

The chart supports persistent volumes for static and media files. Enable persistence:

```yaml
persistence:
  enabled: true
  storageClass: "standard"
  size: 10Gi
```

## SSL/TLS Configuration

For production deployments, configure cert-manager for automatic SSL certificates:

```bash
# Install cert-manager
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.0/cert-manager.yaml

# Create ClusterIssuer
kubectl apply -f - <<EOF
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: your-email@example.com
    privateKeySecretRef:
      name: letsencrypt-prod
    solvers:
    - http01:
        ingress:
          class: nginx
EOF
```

## Monitoring

Enable monitoring with Prometheus:

```yaml
monitoring:
  enabled: true
  serviceMonitor:
    enabled: true
```

## Backup

Configure automated backups:

```yaml
backup:
  enabled: true
  schedule: "0 2 * * *"
  retention: 7
```

## Uninstallation

```bash
helm uninstall sol-web
```

## Troubleshooting

### Check pod status

```bash
kubectl get pods -l app.kubernetes.io/instance=sol-web
```

### View logs

```bash
# Django logs
kubectl logs -l app.kubernetes.io/component=django

# Celery worker logs
kubectl logs -l app.kubernetes.io/component=celery-worker
```

### Access Django shell

```bash
kubectl exec -it deploy/sol-web-django -- python manage.py shell
```

### Run database migrations manually

```bash
kubectl exec -it deploy/sol-web-django -- python manage.py migrate
```

## Support

For issues and feature requests, please open an issue in the project repository.
