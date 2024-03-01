from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend

User = get_user_model()


class EmailBasedAuthBackend(BaseBackend):
    """
    Authenticate using an e-mail address or username.
    """

    def authenticate(self, request, username, password, **kwargs):
        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            return None

        if user.is_active and user.check_password(password or ""):
            return user

        return None

    def get_user(self, user_id: int):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
