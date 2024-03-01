from urllib.parse import urlencode

from decouple import config
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.urls import reverse
from drf_spectacular.utils import extend_schema
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from apps.core.mixins import ApiErrorsMixin, PublicApiMixin
from apps.core.utils import save_image_from_url
from apps.google_oauth2.services import (
    google_get_access_token,
    google_get_user_info,
)
from apps.users.models import UserProfile

User = get_user_model()


@extend_schema(tags=["Google OAuth2"])
class GoogleLoginRedirectApi(PublicApiMixin, APIView):
    def get(self, request, *args, **kwargs):
        domain = config("DJANGO_DOMAIN")
        api_uri = reverse("google-oauth2:google-callback")
        redirect_uri = f"{domain}{api_uri}"
        print(redirect_uri)

        params = {
            "client_id": config("GOOGLE_OAUTH2_CLIENT_ID"),
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "scope": "https://www.googleapis.com/auth/userinfo.email "
            "https://www.googleapis.com/auth/userinfo.profile",
            "access_type": "offline",
            "prompt": "consent",
        }

        return redirect(
            f"https://accounts.google.com/o/oauth2/v2/auth?{urlencode(params)}"
        )


@extend_schema(tags=["Google OAuth2"])
class GoogleLoginApi(PublicApiMixin, ApiErrorsMixin, APIView):
    class InputSerializer(serializers.Serializer):
        code = serializers.CharField(required=False)
        error = serializers.CharField(required=False)

    def create_user_with_profile(self, user_email, user_info):
        username_base = user_email.split("@")[0]
        username = username_base
        suffix = 1

        while User.objects.filter(username=username).exists():
            username = f"{username_base}{suffix}"
            suffix += 1

        user, created = User.objects.get_or_create(
            email=user_email,
            defaults={
                "username": username,
                "first_name": user_info["given_name"],
                "last_name": user_info["family_name"],
                "password": User.objects.make_random_password(),
            },
        )

        if created:
            user_profile = UserProfile.objects.create(user=user)
            save_image_from_url(
                user_profile,
                user_info["picture"],
                f"{user.username}_{user_profile.id}.jpg",
            )
        return user

    def get(self, request, *args, **kwargs):
        input_serializer = self.InputSerializer(data=request.GET)
        input_serializer.is_valid(raise_exception=True)

        validated_data = input_serializer.validated_data
        code = validated_data.get("code")
        error = validated_data.get("error")

        login_url = f'{config("BASE_FRONTEND_URL")}/login'

        if error or not code:
            params = urlencode({"error": error})
            return redirect(f"{login_url}?{params}")

        domain = config("DJANGO_DOMAIN")
        api_uri = reverse("google-oauth2:google-callback")
        redirect_uri = f"{domain}{api_uri}"

        access_token = google_get_access_token(code, redirect_uri)
        user_data = google_get_user_info(access_token)

        user = self.create_user_with_profile(user_data["email"], user_data)
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        cookies = [
            ("access", access_token),
            ("refresh", str(refresh)),
            ("user_id", user.id),
            ("profile_id", user.profile.id),
            ("first_name", user.first_name),
            ("last_name", user.last_name),
            ("image", user.profile.profile_image_url),
        ]

        response = redirect(config("BASE_FRONTEND_URL"))
        for key, value in cookies:
            response.set_cookie(
                key=key,
                value=value,
                httponly=False,
                domain="hobyloc.com",
            )

        return response
