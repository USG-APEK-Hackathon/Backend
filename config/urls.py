from decouple import config
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path, reverse_lazy
from django.views.generic.base import RedirectView
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework_simplejwt.views import TokenBlacklistView

from apps.users.views import (
    CustomTokenObtainPairView,
)
from apps.aidetect.views import ProcessMessageView

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path(
        "api-auth/",
        include("rest_framework.urls", namespace="rest_framework"),
    ),
    # Main API Endpoints
    path(
        "api/v1/",
        include("config.routers", namespace="api-router"),
    ),
    path(
        "api/v1/process-message/",
        ProcessMessageView.as_view(),
    ),
    path(
        "api/v1/google-oauth2/",
        include("apps.google_oauth2.urls", namespace="google-oauth2"),
    ),
    # JWT Auth
    path(
        "api/jwt/create/",
        CustomTokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path("api/", include("djoser.urls.jwt")),
    path(
        "api/jwt/blacklist/",
        TokenBlacklistView.as_view(),
        name="token_blacklist",
    ),
    # Swagger
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    # the following is for the root url
    re_path(
        r"^$",
        RedirectView.as_view(url=reverse_lazy("swagger-ui"), permanent=False),
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
