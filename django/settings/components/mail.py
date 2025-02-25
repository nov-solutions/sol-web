import os

USE_PRODUCTION_EMAIL = os.getenv("ENVIRONMENT") == "prod"

if USE_PRODUCTION_EMAIL:
    # SendGrid
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.sendgrid.net")  # or "smtp.gmail.com"
    EMAIL_PORT = 587
    EMAIL_HOST_USER = os.getenv(
        "EMAIL_HOST_USER", ""
    )  # SendGrid username or Gmail email
    EMAIL_HOST_PASSWORD = os.getenv(
        "EMAIL_HOST_PASSWORD", ""
    )  # SendGrid password or Gmail app password
    EMAIL_USE_TLS = True

else:
    # local file-based backend for development
    EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
    EMAIL_FILE_PATH = "/app/mail/dummy-mail/"

DEFAULT_FROM_EMAIL = "Patriot Owned Businesses <noreply@patriotownedbusinesses.net>"
