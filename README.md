# Sol

Sol is a web app SDK that enables developers to create reliable, robust, and responsive web apps in minutes.

© nov

## Architecture
### Cloud Infrastructure
**AWS**, a cloud computing services company, provides cloud services, such as application hosting, for the web app. The AWS CDK is used to provision most of the resources needed to run the web app in the cloud.

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
**Next.js**, a React web framework, enables server-side rendering of React components and serves as the interface between the presentation and application layers via file system-based routing.
**Tailwind CSS**, a utility-first, class-based CSS framework, simplifies the process of styling markup in the presentation layer.\
**daisyUI**, a component library for Tailwind CSS, provides several pre-built, customizable components for typical UI elements.

### Web Server
**Nginx**, an open-source web server, acts as a reverse proxy that routes both external and internal traffic to the appropriate layer of the web app.

## Setup

0. Clone the repository

1. Populate the keys in the `.env` and `.prod.env` files with appropriate values for the project

2. Run `python find_replace.py` in the root directory

3. Delete "find_replace.py"

4. Address all of the repo-wide `TODO`s

5. Replace all instances of `newsolwebapp.com` with the domain of the project

6. Add "apple_touch_icon.png" and "favicon.png" to `nextjs/public/static/assets/img`

7. Run `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'` in /django to generate a Django secret key. Add it to the `.env` and `.prod.env` files

8. Run `pre-commit install` in the root directory

## Operation

### Local Development
0. Run the appropriate `make` command (`make dev` or `make prod`) in the root directory

1. Access the web app via `localhost`

### Production Deployment
#### One-Time Setup
0. Run `python app.py` in `/cdk` to provision AWS resources

1. Acquire a domain name

2. Execute `cert.sh` in the root directory to generate a TLS certificate for the domain. Rename the output private key to `<project name>-key` and place it in the root directory.

#### Routine Deployment
0. Execute `deploy.sh` in the root directory to transfer and synchronize files and directories from your computer to the AWS EC2 instance

1. Execute `ssh.sh` in the root directory to open a terminal connection from your computer to the AWS EC2 instance

2. Run `cd app` to access the web app files inside of the Docker container on the AWS EC2 instance

3. Run `docker compose up --build` to rebuild the app containers with the synchronized files
