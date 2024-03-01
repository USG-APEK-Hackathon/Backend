from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    """Default user for this project."""

    def __str__(self):
        return self.username


class UserProfile(models.Model):
    """User profile."""

    user = models.OneToOneField(
        "users.User", related_name="profile", on_delete=models.CASCADE
    )
    birth_date = models.DateField(_("birth_date"), null=True, blank=True),
    profile_image = models.ImageField(
        upload_to="profile_images/", null=True, blank=True,
    )

    def __str__(self):
        return self.user.username

    @property
    def profile_image_url(self):
        if self.profile_image:
            return self.profile_image.url
        return None
