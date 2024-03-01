from django.conf import settings
from rest_framework.routers import BaseRouter, DefaultRouter, SimpleRouter
from apps.aidetect.views import HumanHelthViewSet

from apps.users.views import UserProfileViewSet

app_name = "api-router"

router: BaseRouter

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("profiles", UserProfileViewSet, basename="profile")
router.register("human-health", HumanHelthViewSet, basename="humanhelth")

urlpatterns = router.urls + []
