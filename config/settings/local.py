import os
import socket

from config.settings.common import Common

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Local(Common):
    DEBUG = True

    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS = [ip[:-1] + "1" for ip in ips] + ["127.0.0.1"]

    # Testing
    INSTALLED_APPS = Common.INSTALLED_APPS
    MIDDLEWARE = Common.MIDDLEWARE

    INSTALLED_APPS += (
        "django_nose",
        "debug_toolbar",
    )
    MIDDLEWARE += ("debug_toolbar.middleware.DebugToolbarMiddleware",)
    TEST_RUNNER = "django_nose.NoseTestSuiteRunner"
    NOSE_ARGS = [
        BASE_DIR,
        "-s",
        "--nologcapture",
        "--with-coverage",
        "--with-progressive",
        "--cover-package=HobyLoc",
    ]

    # Mail
    EMAIL_HOST = "localhost"
    EMAIL_PORT = 1025
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
