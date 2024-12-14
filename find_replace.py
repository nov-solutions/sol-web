import os


def find_replace():
    """
    Replaces instances of "sol" with the value of SITE_NAME in ".env"
    """

    with open(".env", "r") as f:
        file = f.readlines()
    for line in file:
        key = line.split("=")[0]
        print(key)
        if key == "NEXT_PUBLIC_SITE_NAME":
            replace = line.split("=")[1].strip()
            break
    if not replace:
        raise ValueError("SITE_NAME not found in .env file")
    print("Replacing instances of sol with " + replace)

    for root, dirs, files in os.walk("."):
        for file in files:
            if (
                file == "find_replace.py"
                or ".git/" in os.path.join(root, file)
                or ".pyc" in os.path.join(root, file)
                or ".terraform" in os.path.join(root, file)
                or ".png" in os.path.join(root, file)
                or ".ico" in os.path.join(root, file)
                or ".eot" in os.path.join(root, file)
                or ".ttf" in os.path.join(root, file)
                or ".woff" in os.path.join(root, file)
                or ".gif" in os.path.join(root, file)
            ):
                continue
            print("file: " + file)
            with open(os.path.join(root, file), "r") as f:
                text = f.read()
            with open(os.path.join(root, file), "w") as f:
                f.write(text.replace("sol-web", replace + "-web"))


if __name__ == "__main__":
    find_replace()
