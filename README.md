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
**Django**, a Python web framework, expresses this logic and serves as the interface between the presentation and data layers via the Model-View-Template design pattern.\
**Celery**, a Python task queue, handles asynchronous tasks in the web app. Celery is configured to use Redis as its message broker.

### Presentation Layer

**Typescript**, a superset of Javascript, the core programming language of the Internet, handles the frontend logic of the web app.\
**React**, a Javascript and Typescript library, bundles this logic and provides a component-based framework for expressing it.\
**Next.js**, a React web framework, enables server-side rendering of React components and serves as the interface between the presentation and application layers via file system-based routing.\
**Tailwind CSS**, a utility-first, class-based CSS framework, simplifies the process of styling markup in the presentation layer.\
**shadcn/ui**, a component library for Tailwind CSS, provides several pre-built, customizable UI components.

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

2. Upload the production secrets referenced in `.github/workflows/deploy.yaml` and `.github/workflows/test.yaml` (except for `SECRET_KEY`) to the GitHub repository

3. Run `python app.py` in `/cdk` to provision AWS resources for the project

4. Replace all project-wide instances of `IP_ADDRESS` with the IP address of the project's AWS EC2 instance

5. Acquire a domain name

6. Execute `cert.sh` in the root directory to generate a TLS certificate for the domain. Rename the output private key to `app-key.pem` and place it in the root directory

7. Run `make key-pair` in the root directory to generate an SSH key pair

8. Push code to the master branch of the repository to initialize the project's files on the AWS EC2 instance

9. Run `make ssh` in the root directory to open a terminal connection to the AWS EC2 instance. Change directories to `/app` to access the project's files

10. Run `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'` in `/django` to generate a Django secret key that can be used in production. Upload the secret key to the GitHub repository and name it `SECRET_KEY`
