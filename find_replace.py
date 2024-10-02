# the purpose of this script is simple
# it iterates through every file in a directory
# for each file it looks for the string:
# and replaces it with the string argument passed to the script

import os
import shutil


def find_replace():
    """
    Replaces instances of NEWSOLWEBAPP with the value of SITE_NAME in the .env file.
    Also, renames ./django/newsolwebapp folder to the value of SITE_NAME.
    """

    # read .env and get value of SITE_NAME
    with open(".env", "r") as f:
        file = f.readlines()
    for line in file:
        key = line.split("=")[0]
        print(key)
        if key == "SITE_NAME":
            replace = line.split("=")[1].strip()
            break
    if not replace:
        raise ValueError("SITE_NAME not found in .env file")
    print("Replacing instances of NEWSOLWEBAPP with " + replace)

    # walks through directory, replaces instances of NEWSOLWEBAPP with SITE_NAME
    for root, dirs, files in os.walk("."):
        for file in files:
            if file == "find_replace.py" or ".git" in os.path.join(root, file):
                continue
            with open(os.path.join(root, file), "r") as f:
                text = f.read()
            with open(os.path.join(root, file), "w") as f:
                f.write(text.replace("NEWSOLWEBAPP", replace))

    # rename ./django/newsolwebapp to SITE_NAME
    shutil.move("./django/newsolwebapp", f"./django/{replace}")


if __name__ == "__main__":
    find_replace()
