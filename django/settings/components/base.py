import os

from decouple import config

ENVIRONMENT = config("ENVIRONMENT")
SITE_BASE_DOMAIN = config("NEXT_PUBLIC_SITE_BASE_DOMAIN")
SITE_DOMAIN = config("SITE_DOMAIN")
SECRET_KEY = config("SECRET_KEY")
POSTGRES_DB = config("POSTGRES_DB")
POSTGRES_USER = config("POSTGRES_USER")
POSTGRES_PASSWORD = config("POSTGRES_PASSWORD")
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"

if ENVIRONMENT == "dev":
    DEBUG = True
elif ENVIRONMENT == "prod":
    DEBUG = False

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

ASGI_APPLICATION = "web.asgi.application"

INSTALLED_APPS = [
    "daphne",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.staticfiles",
    "django.contrib.messages",
    "corsheaders",
    # drf
    "rest_framework",
    "django_extensions",
    "django_filters",
    "drf_spectacular",
    # core logic
    "core.apps.CoreConfig",
    # users and auth
    "user.apps.UserConfig",
    # automated api docs
    "spectacular.apps.SpectacularSwaggerConfig",
    # async task queueing
    "celeryapp.apps.CeleryAppConfig",
    # e-mail
    "mail.apps.MailConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": POSTGRES_DB,
        "USER": POSTGRES_USER,
        "PASSWORD": POSTGRES_PASSWORD,
        "HOST": "postgres",
        "PORT": 5432,
    }
}

USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

ALLOWED_HOSTS = [
    "django",
    SITE_DOMAIN,
    "." + SITE_DOMAIN,
]

CSRF_TRUSTED_ORIGINS = [
    SITE_BASE_DOMAIN,
]

CORS_ALLOWED_ORIGINS = [
    SITE_BASE_DOMAIN,
]

CORS_ALLOW_CREDENTIALS = True

ROOT_URLCONF = "web.urls"

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer",),
    "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]
