#!/bin/bash

source "./.prod.env"

if ! command -v gh &> /dev/null
then
    echo "GitHub CLI (gh) could not be found. Please install it."
    exit 1
fi

ENV_FILE=".prod.env"

while IFS= read -r line || [[ -n "$line" ]]; do
    if [[ -n "$line" ]] && [[ $line != \#* ]]; then
        key=$(echo "$line" | cut -d '=' -f 1)
        value=$(echo "$line" | cut -d '=' -f 2-)
        echo "Setting $key for $GITHUB_REPO..."
        echo "$value" | gh secret set "$key" --repos "$GITHUB_REPO" --body "$value"
    fi
done < "$ENV_FILE"
