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

3. Run `python find_replace.py` in the root directory

4. Address all of the repo-wide `TODO`s

5. Replace all instances of `newsolwebapp.com` with the domain of the project

6. Add "apple_touch_icon.png" and "favicon.png" to `nextjs/public/static/assets/img`

7. Run `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'` in /django to generate a Django secret key. Add it to the `.env` and `.prod.env` files
