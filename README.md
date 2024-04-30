# Sol

## Setup

1. Clone the repository

2. Populate the keys in the `.env` and `.prod.env` files with appropriate values for the project

3. Run `python find_replace.py` in the root directory

4. Delete "find_replace.py"

5. Address all of the repo-wide `TODO`s

6. Replace all instances of `newsolwebapp.com` with the domain of the project

7. Add "apple_touch_icon.png" and "favicon.png" to `nextjs/public/static/assets/img`

8. Run `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'` in /django to generate a Django secret key. Add it to the `.env` and `.prod.env` files
