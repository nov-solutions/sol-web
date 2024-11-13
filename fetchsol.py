import os

import requests

sol_config = {}


file_names = [
    # Add file names here, e.g., "django/base_urls.py"
]

base_url = "https://files.grav.solutions/files/"

for file_name in file_names:
    url = f"{base_url}{file_name}"
    response = requests.get(url)

    if response.status_code == 200:
        file_path = os.path.join(".", file_name)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "wb") as file:
            file.write(response.content)
        print(f"Successfully saved {file_name}")
    else:
        print(f"Failed to retrieve {file_name}, status code: {response.status_code}")
