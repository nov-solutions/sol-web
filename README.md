# Sol

## Setup
1. Clone the repository
2. Create an `.env` file in the root directory and populate it with the following essential keys and their respective values for the project:

```
ENVIRONMENT=dev

SITE_NAME=
SITE_DESCRIPTION=
SITE_TAGLINE=
SITE_BASE_DOMAIN=localhost
SECRET_KEY=
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
```

3. Create a `.prod.env` file in the root directory and populate it with the following essential keys and their respective values for the project:

```
ENVIRONMENT=prod
GITHUB_REPO=

SITE_NAME=
SITE_DESCRIPTION=
SITE_TAGLINE=
SITE_BASE_DOMAIN=
SECRET_KEY=
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
```

4. Rename the Django app from `newsolwebapp` to the value of `SITE_NAME` in the environment files

5. Address all of the repo-wide `TODO`s

6. Replace all instances of `NEWSOLWEBAPP` with the name of the project

7. Replace all instances of `newsolwebapp.com` with the domain of the project

8. Add "apple_touch_icon.png" and "favicon.png" to `nextjs/public/static/assets/img`

9. Run `npm install` in the root directory

10. Run `npm install` in /nextjs