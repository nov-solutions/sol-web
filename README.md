# Sol

Sol is an all-in-one template that enables developers to create robust, reliable and responsive web apps in minutes.

© [nov](https://github.com/nov-solutions)

## Architecture

### Cloud Infrastructure

**AWS**, a cloud computing services company, provides cloud services, such as application hosting, for the web app. The AWS CDK is used to provision most of the resources needed to run the web app in the cloud.

### Continuous Integration and Continuous Deployment

**GitHub Actions**, a CI/CD platform, automates the process of building, testing, and deploying the web app to the cloud. The `.github/workflows` directory contains the configuration files for the GitHub Actions workflows that run when code is pushed to the primary branch of the repository.

### Virtualization and Containerization

**Docker**, a bundle of PAAS products, enables the virtualization and containerization of the web app and standardizes the local development and production deployment environments.

### Data Layer

**PostgreSQL**, an open-source ORDBMS, handles persistent data storage.\
Data is interacted with through Django's ORM in the application layer.

### Application Layer

**Python**, a general-purpose, object-oriented programming language, handles the backend logic of the web app.\
**Django**, a Python web framework, expresses this logic and serves as the interface between the presentation and data layers via the Model-View-Template design pattern.
**Celery**, a Python task queue, handles asynchronous tasks in the web app. Celery is configured to use Redis as its message broker.\

### Presentation Layer

**Typescript**, a superset of Javascript, the core programming language of the Internet, handles the frontend logic of the web app.\
**React**, a Javascript and Typescript library, bundles this logic and provides a component-based framework for expressing it.\
**Next.js**, a React web framework, enables server-side rendering of React components and serves as the interface between the presentation and application layers via file system-based routing.
**Tailwind CSS**, a utility-first, class-based CSS framework, simplifies the process of styling markup in the presentation layer.\
**daisyUI**, a component library for Tailwind CSS, provides several pre-built, customizable components for typical UI elements.

### Web Server

**Nginx**, an open-source web server, acts as a reverse proxy that routes both external and internal traffic to the appropriate layer of the web app.

## Setup

0. Clone the repository

1. Install [Docker Engine](https://docs.docker.com/engine/install/) if you haven't already

2. Replace the values in `.env` with appropriate values for the local build of the project

3. Run `python find_replace.py` in the root directory

4. Delete `find_replace.py`

5. Address all of the repository-wide `TODO`s

6. Update the web app manifest at `/nextjs/public/manifest.json` with appropriate values for the project

7. Replace the placeholder `logo.png` and `wordmark.png` in `nextjs/public/static/assets/img/logos` with the appropriate assets for the project

8. Replace the placeholder `social.png,` `favicon.png`, and `apple_touch_icon.png` in `nextjs/public/static/assets/img` with the appropriate assets for the project

9. Run `pre-commit install` in the root directory

## Operation

### Local Development

0. Run `make` to build the project's Docker images and start the project's Docker containers

1. Access the web app via localhost

### Production Deployment

#### One-Time Setup

0. Replace the `CDK_ACCOUNT` and `CDK_REGION` values in `.env` with the appropriate values for the AWS account and region in which the project will be deployed

1. Replace the values in `.github/workflows/deploy.yaml` and `.github/workflows/test.yaml` with appropriate values for the production build of the project

2. Upload the production secrets referenced in `.github/workflows/deploy.yaml` and `.github/workflows/test.yaml` to the GitHub repository. Run `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'` to generate a Django secret key that can be used in production.

3. Run `make key-pair` in the root directory to generate an SSH key pair. change the permission `sudo chmod 400 app.pem`. Run `make cdk-deploy` in the root directory to provision AWS resources for the project

4. Replace `52.38.15.163` (sol's IP address) across the repository with the IP address of the project's AWS EC2 instance, it can be found in `cdk/outputs.json`

5. Acquire a domain name, setup dns

6. while ssh on the server, Execute `cert.sh` in the root directory to generate a TLS certificate for the domain.

7. install docker on the server

8. if the pipelines are setup correctly as in the earlier step, pushing to master will trigger the deployment of the files to the server and will start the containers
