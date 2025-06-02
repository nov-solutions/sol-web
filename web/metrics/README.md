# Metrics App

This Django app provides Prometheus metrics using `django_prometheus`.

## Features

- **Automatic Django Metrics**: Request/response times, database queries, cache operations
- **Health Checks**: Simple health, readiness, and liveness endpoints for Kubernetes

## Endpoints

- `/metrics/` - Prometheus metrics endpoint (provided by django_prometheus)
- `/metrics/health/` - Health check
- `/metrics/readiness/` - Readiness probe
- `/metrics/liveness/` - Liveness probe

## Setup

1. Add `django_prometheus` and `metrics` to INSTALLED_APPS
2. Add django_prometheus middleware to MIDDLEWARE
3. Include metrics URLs in your main urls.py

See Django settings configuration for details.
