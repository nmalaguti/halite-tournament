"""
Django settings for project project.

Generated by 'django-admin startproject' using Django 4.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path

import sentry_sdk
from configurations import Configuration, values
from sentry_sdk.integrations.django import DjangoIntegration

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Base(Configuration):
    AUTH_USER_MODEL = "tournament.User"

    INSTALLED_APPS = [
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        "social_django",
        "crispy_forms",
        "crispy_bootstrap3",
        "rest_framework",
        "rest_framework.authtoken",
        "django_extensions",
        "tournament",
    ]

    MIDDLEWARE = [
        "django.middleware.security.SecurityMiddleware",
        "whitenoise.middleware.WhiteNoiseMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
        "social_django.middleware.SocialAuthExceptionMiddleware",
    ]

    ROOT_URLCONF = "project.urls"

    TEMPLATES = [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [],
            "APP_DIRS": True,
            "OPTIONS": {
                "builtins": [
                    "django.templatetags.static",
                    "crispy_forms.templatetags.crispy_forms_tags",
                    "tournament.templatetags.tournament_extras",
                ],
                "context_processors": [
                    "django.template.context_processors.debug",
                    "django.template.context_processors.request",
                    "django.contrib.auth.context_processors.auth",
                    "django.contrib.messages.context_processors.messages",
                    "social_django.context_processors.backends",
                    "social_django.context_processors.login_redirect",
                ],
            },
        },
    ]

    WSGI_APPLICATION = "project.wsgi.application"

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

    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
            },
        },
        "root": {
            "handlers": ["console"],
            "level": "INFO",
        },
    }

    LANGUAGE_CODE = "en-us"

    TIME_ZONE = "UTC"

    USE_I18N = True

    USE_TZ = True

    STATIC_URL = "static/"
    STATIC_ROOT = BASE_DIR / "staticfiles"

    DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

    AUTHENTICATION_BACKENDS = [
        "social_core.backends.github.GithubOAuth2",
        "django.contrib.auth.backends.ModelBackend",
    ]

    SOCIAL_AUTH_GITHUB_LOGIN_REDIRECT_URL = "tournament:profile"

    AWS_STORAGE_BUCKET_NAME = "halite-tournament-storage"
    AWS_S3_REGION_NAME = "us-east-1"

    STORAGES = {
        "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"
        },
    }

    CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap3"

    CRISPY_TEMPLATE_PACK = "bootstrap3"

    LOGIN_URL = "/login/"


class CollectStatic(Base):
    SECRET_KEY = "django-insecure-vt&hc$fjig2n20^tv=@0)2@hq&^*lozpfa_m(_f61a-6@k(*fa"


class Secrets(Base):
    SECRET_KEY = values.SecretValue()

    SOCIAL_AUTH_GITHUB_KEY = values.SecretValue()
    SOCIAL_AUTH_GITHUB_SECRET = values.SecretValue()

    AWS_S3_ACCESS_KEY_ID = values.SecretValue()
    AWS_S3_SECRET_ACCESS_KEY = values.SecretValue()

    GITHUB_WORKFLOW_TOKEN = values.SecretValue()
    GITHUB_READ_PACKAGES_TOKEN = values.SecretValue()

    DOCKER_PUBLIC_READ_USERNAME = values.SecretValue()
    DOCKER_PUBLIC_READ_TOKEN = values.SecretValue()


class Dev(Secrets):
    DOTENV = BASE_DIR / ".env"

    DEBUG = True

    ALLOWED_HOSTS = ["*"]
    INTERNAL_IPS = ["127.0.0.1"]

    MEDIA_URL = "media/"
    MEDIA_ROOT = BASE_DIR / "mediafiles"

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


class DevProd(Dev):
    DATABASES = values.DatabaseURLValue(environ_prefix="DJANGO", ssl_require=True)

    STORAGES = {
        "default": {"BACKEND": "storages.backends.s3boto3.S3Boto3Storage"},
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"
        },
    }


class Prod(Secrets):
    DEBUG = False

    SECRET_KEY = values.SecretValue()

    ALLOWED_HOSTS = values.ListValue(["halite-tournament.fly.dev"])

    USE_X_FORWARDED_HOST = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

    DATABASES = values.DatabaseURLValue(environ_prefix="DJANGO", ssl_require=True)

    STORAGES = {
        "default": {"BACKEND": "storages.backends.s3boto3.S3Boto3Storage"},
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"
        },
    }

    @classmethod
    def post_setup(cls):
        """Sentry initialization"""
        super(Prod, cls).post_setup()

        sentry_sdk.init(
            dsn="https://58fb964e22e140a7b5350d8c09203d23@o4505465961119744.ingest.sentry.io/4505465962627072",
            integrations=[
                DjangoIntegration(),
            ],
            # Set traces_sample_rate to 1.0 to capture 100%
            # of transactions for performance monitoring.
            # We recommend adjusting this value in production.
            traces_sample_rate=0,
            # If you wish to associate users to errors (assuming you are using
            # django.contrib.auth) you may enable sending PII data.
            send_default_pii=True,
        )
