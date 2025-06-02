# Prometheus Metrics

This Django app provides Prometheus metrics using `django_prometheus`.

## Features

- **Automatic Django Metrics**: Request/response times, database queries, cache operations

## Endpoints

- `/api/metrics/` - Prometheus metrics endpoint (provided by django_prometheus)

## Setup

1. Add `django_prometheus` and `metrics` to INSTALLED_APPS
2. Add django_prometheus middleware to MIDDLEWARE
3. Include metrics URLs in your main urls.py
