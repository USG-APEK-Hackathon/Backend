from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from rest_framework import exceptions as rest_exceptions

from apps.core.utils import get_error_message

User = get_user_model()


class PublicApiMixin:
    authentication_classes = ()
    permission_classes = ()
    serializer_class = None


class ApiErrorsMixin:
    expected_exceptions = {
        ValueError: rest_exceptions.ValidationError,
        ValidationError: rest_exceptions.ValidationError,
        PermissionError: rest_exceptions.PermissionDenied,
        User.DoesNotExist: rest_exceptions.NotAuthenticated,
    }

    def handle_exception(self, exc):
        if isinstance(exc, tuple(self.expected_exceptions.keys())):
            drf_exception_class = self.expected_exceptions[exc.__class__]
            drf_exception = drf_exception_class(get_error_message(exc))

            return super().handle_exception(drf_exception)

        return super().handle_exception(exc)
