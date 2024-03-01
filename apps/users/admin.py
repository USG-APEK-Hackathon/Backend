from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.users.models import User, UserProfile


class UserAdmin(UserAdmin):
    list_display = (
        "id",
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
    )


class UserProfileAdmin(admin.ModelAdmin):
    """
    Admin class for managing user profiles.
    """

    list_display = ("id", "username", "email")

    def username(self, obj):
        return obj.user.username

    def email(self, obj):
        return obj.user.email

    username.short_description = "Username"
    email.short_description = "Email"



admin.site.register(User, UserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
