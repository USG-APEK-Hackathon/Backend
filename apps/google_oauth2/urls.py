from django.urls import path

from apps.google_oauth2.apis import GoogleLoginApi, GoogleLoginRedirectApi

app_name = "google-oauth2"

urlpatterns = [
    path(
        "redirect/",
        GoogleLoginRedirectApi.as_view(),
        name="google-redirect",
    ),
    path("callback/", GoogleLoginApi.as_view(), name="google-callback"),
]
