from corsheaders.defaults import default_headers
from decouple import Csv, config

from config.settings.common import Common


class Production(Common):
    INSTALLED_APPS = Common.INSTALLED_APPS
    REST_FRAMEWORK = Common.REST_FRAMEWORK

    SECRET_KEY = config("DJANGO_SECRET_KEY")
    # Site
    # https://docs.djangoproject.com/en/2.0/ref/settings/#allowed-hosts
    ALLOWED_HOSTS = config("DJANGO_ALLOWED_HOSTS", cast=Csv())
    ADMIN_URL = config("DJANGO_ADMIN_URL")

    # CORS
    CORS_URLS_REGEX = r"^/api/.*$"
    CORS_ALLOW_CREDENTIALS = True
    CORS_ORIGIN_WHITELIST = config(
        "CORS_ORIGIN_WHITELIST", cast=Csv(), default=["http://localhost:3000"]
    )
    CORS_ALLOWED_ORIGINS = config(
        "CORS_ALLOWED_ORIGINS", cast=Csv(), default=["localhost:3000"]
    )
    CORS_ALLOW_ALL_ORIGINS = config(
        "CORS_ALLOW_ALL_ORIGINS", default=True, cast=bool
    )  # noqa E501
    CORS_ALLOW_METHODS = (
        "DELETE",
        "GET",
        "OPTIONS",
        "PATCH",
        "POST",
        "PUT",
    )
    CORS_ALLOW_HEADERS = list(default_headers) + ["Set-Cookie"]

    # CSRF
    CSRF_TRUSTED_ORIGINS = config("CSRF_TRUSTED_ORIGINS", cast=Csv())

    CSRF_USE_SESSIONS = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    CSRF_COOKIE_SAMESITE = None
    SESSION_COOKIE_SAMESITE = None

    STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",  # noqa E501
        },
    }

    REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = (
        "rest_framework.renderers.JSONRenderer",
    )
