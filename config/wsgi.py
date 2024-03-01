"""
WSGI config for this project.
It exposes the WSGI callable as a module-level variable named ``application``.
For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/gunicorn/
"""
import os

from decouple import config

django_settings_module = config(
    "DJANGO_SETTINGS_MODULE", default="config.settings.local"
)
django_configuration = config("DJANGO_CONFIGURATION", default="Local")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", django_settings_module)
os.environ.setdefault("DJANGO_CONFIGURATION", django_configuration)

from configurations.wsgi import get_wsgi_application  # noqa

application = get_wsgi_application()
