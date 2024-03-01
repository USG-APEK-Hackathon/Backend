from django.conf import settings
from rest_framework.routers import BaseRouter, DefaultRouter, SimpleRouter

from apps.users.views import UserProfileViewSet

app_name = "api-router"

router: BaseRouter

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("profiles", UserProfileViewSet, basename="profile")

urlpatterns = router.urls + []
