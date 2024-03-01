from rest_framework import permissions


class IsUserProfile(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    message = "You are not user profile owner."

    def has_permission(self, request, view):
        return bool(
            request.user.is_authenticated and hasattr(request.user, "profile")
        )
