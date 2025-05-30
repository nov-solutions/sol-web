# Sol

Sol is an all-in-one template that enables developers to create robust, reliable and responsive web apps in minutes.

© [nov](https://github.com/nov-solutions)

## Getting Started

### Local Development

0. Run `make dev` to build the project's Docker images and start the project's Docker containers

1. Access the web app `http://localhost`

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

### Load Balancer

**Nginx**, an open-source web server, acts as a reverse proxy that routes both external and internal traffic to the appropriate layer of the web app.
