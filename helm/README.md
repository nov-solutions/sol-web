# Sol Web Helm Chart - Minikube Setup

This guide explains how to run the Sol Web application using Helm on Minikube.

## Prerequisites

1. **Minikube** - [Installation Guide](https://minikube.sigs.k8s.io/docs/start/)
2. **Helm 3.x** - [Installation Guide](https://helm.sh/docs/intro/install/)
3. **kubectl** - Usually installed with Minikube

## Quick Start

### 1. Build Docker Images Locally

First, build all the Docker images that the Helm chart will use:

```bash
# From the project root directory
docker compose build

# Tag images for local Kubernetes
docker tag sol-web-nextjs:latest sol-web-nextjs:latest
docker tag sol-web-django:latest sol-web-django:latest
docker tag sol-web-nginx:latest sol-web-nginx:latest
```

### 2. Start Minikube

```bash
# stop previous Minikube instance if running, might need to delete also
minikube stop
# Start Minikube with sufficient resources
minikube start --driver=docker --kubernetes-version=v1.28.0 --cpus=4 --memory=8192

# Enable ingress addon (optional, for ingress support)
minikube addons enable ingress
```


### 3. Load Images into Minikube

```bash
# Use Minikube's Docker daemon
eval $(minikube docker-env)

# Build images directly in Minikube's Docker environment
docker compose build
```

### 4. Add Helm Dependencies

```bash
cd helm
helm dependency update
```

### 6. Install the Chart

```bash
# Create namespace
kubectl create namespace sol-web

# Install the chart
helm install sol-web . -f values.local.yaml -n sol-web

# Or upgrade if already installed
helm upgrade sol-web . -f values.local.yaml -n sol-web
```

### 7. Access the Application

```bash
# Get the URL for the nginx service
minikube service sol-web-nginx -n sol-web --url

# Alternative: Use port-forwarding
kubectl port-forward -n sol-web svc/sol-web-nginx 8080:80
```

Then access the application at:

- Frontend: <http://localhost:8080>
- API: <http://localhost:8080/api>

## Common Operations

### Check Pod Status

```bash
kubectl get pods -n sol-web
kubectl describe pod <pod-name> -n sol-web
kubectl logs <pod-name> -n sol-web
```

### Run Django Migrations

```bash
# Get Django pod name
DJANGO_POD=$(kubectl get pods -n sol-web -l app.kubernetes.io/name=sol-web,app.kubernetes.io/component=django -o jsonpath='{.items[0].metadata.name}')

# Run migrations
kubectl exec -it $DJANGO_POD -n sol-web -- python manage.py migrate

# Create superuser
kubectl exec -it $DJANGO_POD -n sol-web -- python manage.py createsuperuser
```

### Update Configuration

```bash
# After modifying values.local.yaml
helm upgrade sol-web . -f values.local.yaml -n sol-web
```

### Uninstall

```bash
helm uninstall sol-web -n sol-web
kubectl delete namespace sol-web
```

## Troubleshooting

### Minikube-Specific Issues

```bash
# Check Minikube status
minikube status

# View Minikube dashboard
minikube dashboard

# Check if you're using Minikube's Docker daemon
docker context show  # Should show "default" if using Minikube's daemon

# Reset Docker environment (to use host Docker again)
eval $(minikube docker-env -u)
```

### Images Not Found

If Kubernetes can't find your local images:

1. Ensure you're using Minikube's Docker daemon: `eval $(minikube docker-env)`
2. Verify `pullPolicy: Never` is set in values.local.yaml
3. Check image names match exactly with: `docker images`
4. Rebuild images after switching to Minikube's Docker daemon

### Database Connection Issues

```bash
# Check PostgreSQL pod
kubectl logs -n sol-web -l app.kubernetes.io/name=postgresql

# Verify database credentials
kubectl get secret sol-web-postgresql -n sol-web -o yaml
```

### Port Conflicts

If ports are already in use:

```bash
# Use different local ports
kubectl port-forward -n sol-web svc/sol-web-nginx 8081:80
```

### Resource Constraints

For limited local resources, further reduce the resource requests in `values.local.yaml`.

## Development Workflow

1. Make code changes
2. Ensure you're using Minikube's Docker daemon: `eval $(minikube docker-env)`
3. Rebuild affected Docker images: `docker compose build`
4. Delete the affected pods to force recreation:

   ```bash
   kubectl delete pod -n sol-web -l app.kubernetes.io/component=django
   ```

## Using Helm Hooks

For database initialization, you can create a Job:

```yaml
# templates/migrations-job.yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: {{ include "sol-web.fullname" . }}-migrations
  annotations:
    "helm.sh/hook": post-install,post-upgrade
    "helm.sh/hook-weight": "1"
spec:
  template:
    spec:
      restartPolicy: Never
      containers:
      - name: migrations
        image: "{{ .Values.django.image.repository }}:{{ .Values.django.image.tag }}"
        command: ["python", "manage.py", "migrate"]
        env:
          # Include all Django env vars
```

## Additional Resources

- [Helm Documentation](https://helm.sh/docs/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Sol Web Project Documentation](../README.md)
