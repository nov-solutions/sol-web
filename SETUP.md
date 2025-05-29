# Setup

0. Clone the repository

1. Install [Docker Engine](https://docs.docker.com/engine/install/) if you haven't already

2. Replace the values in the `environment` configurations in `docker-compose.yaml` with appropriate values for the development build of the project

3. Run `python find_replace.py` in the root directory

4. Delete `find_replace.py`

5. Address all of the repository-wide `TODO`s

6. Update the web app manifest at `/nextjs/public/manifest.json` with appropriate values for the project

7. Replace the placeholder `logo.png` and `wordmark.png` in `nextjs/public/assets/img/logos` with the appropriate assets for the project

8. Replace the placeholder `social.png,` `favicon.png`, and `apple_touch_icon.png` in `nextjs/public/assets/img` with the appropriate assets for the project

9. Run `pre-commit install` in the root directory

## Infra Setup

0. Configure AWS account values

   - If you haven't already, install [`awscli`](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) on your machine
   - If you haven't already, install [`cdk`](https://docs.aws.amazon.com/cdk/latest/guide/cli.html) on your machine
   - Replace the `CDK_ACCOUNT` and `CDK_REGION` values in `cdk/app.py` with the appropriate values for the AWS account and region in which the project will be deployed

1. Replace the values in `.github/workflows/deploy.yaml` and `.github/workflows/test.yaml` with appropriate values for the production build of the project. Use the local environment variable values in `.env` as a reference

2. Upload the production secrets referenced in `.github/workflows/deploy.yaml` and `.github/workflows/test.yaml` to the GitHub repository

   - Run `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'` in `/django` to generate a Django secret key (`SECRET_KEY`) that can be used in production

3. Generate an SSH key pair

   - Run `make key-pair` in the root directory
   - Update the permissions of the generated `app.pem` file by running `sudo chmod 400 app.pem`

4. Run `make deploy-cdk` in the root directory to provision AWS resources for the project

5. Replace all project-wide instances of `IP_ADDRESS` with the IP address of the project's AWS EC2 instance. The project's IP address can be found in `cdk/outputs.json`

6. Configure the project's domain

   - Acquire a domain name
   - Add an "A" record with a "Host" value of `@` and "Value" value of the IP address of the project's AWS EC2 instance to the domain's DNS settings
   - Add a "CNAME" record with a "Host" value of `www` and "Value" value of the domain name to the domain's DNS settings

7. Replace all instances of `sol.grav.solutions` in `nginx/prod/site.conf` with the domain name of the project

8. Push code to the master branch of the repository to initialize the project's files on the AWS EC2 instance

9. Generate a TLS certificate for the domain

   - Run `make ssh` in the root directory to open a terminal connection to the AWS EC2 instance
   - Navigate to `/app`
   - Make the cert script executable by running `chmod +x cert.sh`
   - Execute `./cert.sh`
