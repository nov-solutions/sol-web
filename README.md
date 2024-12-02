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

### Presentation Layer

**Typescript**, a superset of Javascript, the core programming language of the Internet, handles the frontend logic of the web app.\
**React**, a Javascript and Typescript library, bundles this logic and provides a component-based framework for expressing it.\
**Next.js**, a React web framework, enables server-side rendering of React components and serves as the interface between the presentation and application layers via file system-based routing.\
**Tailwind CSS**, a utility-first, class-based CSS framework, simplifies the process of styling markup in the presentation layer.\
**daisyUI**, a component library for Tailwind CSS, provides several pre-built, customizable components for typical UI elements.

### Web Server

**Nginx**, an open-source web server, acts as a reverse proxy that routes both external and internal traffic to the appropriate layer of the web app.

## Setup

0. Clone the repository

1. Populate the keys in the `.env` file with appropriate values for the project

2. Run `python find_replace.py` in the root directory

3. Delete "find_replace.py"

4. Address all of the repo-wide `TODO`s

5. Add "apple_touch_icon.png," "favicon.png," and "social.png" to `nextjs/public/static/assets/img`

6. Add "logo.png", "wordmark.png", "social.png," "favicon.png", and "apple_touch_icon.png" to `nextjs/public/static/assets/img`

7. Run `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'` in /django to generate a Django secret key. Add it to the `.env` file

8. Run `pre-commit install` in the root directory

## Operation

### Local Development

0. Run `make dev` in the root directory

1. Access the web app via `localhost`

### Production Deployment

#### One-Time Setup

0. Run `python app.py` in `/cdk` to provision AWS resources

1. Acquire a domain name

2. Execute `cert.sh` in the root directory to generate a TLS certificate for the domain. Rename the output private key to `<project name>-key` and place it in the root directory.

#### Routine Deployment

0. Push code to the master branch of the repository

### Production Management

0. Run `make ssh` in the root directory to open a terminal connection to the AWS EC2 instance
