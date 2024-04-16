# Sol

## Setup

1. `git clone git@github.com:nov-solutions/sol.git`

2. fill out the `.env` and `.prod.env` files

3. Run `python find_replace.py`

4. Address all of the repo-wide `TODO`s

5. Replace all instances of `newsolwebapp.com` with the domain of the project

6. Add "apple_touch_icon.png" and "favicon.png" to `nextjs/public/static/assets/img`

7. Run `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'` in /django to generate a Django secret key. Add it to the `.env` and `.prod.env` files
