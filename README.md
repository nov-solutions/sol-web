# Sol

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
