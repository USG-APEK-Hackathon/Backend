from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import generics, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from apps.core.permissions import IsUserProfile

from apps.users.models import UserProfile
from apps.users.permissions import IsOwnerOrAdminOrReadOnly
from apps.users.serializers import (
    CustomTokenObtainPairSerializer,
    UserCreateSerializer,
    UserProfileSerializer,
)


@extend_schema(tags=["profiles"])
class UserProfileViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing UserProfile objects."""

    queryset = (
        UserProfile.objects.select_related("user")
        .prefetch_related("skills")
        .all()
    )
    serializer_class = UserProfileSerializer
    permission_classes = [
        IsOwnerOrAdminOrReadOnly,
    ]

    def get_permissions(self):
        if self.request.method in ["POST", "OPTIONS"]:
            self.permission_classes = [permissions.AllowAny]
        if self.action in ["me"]:
            self.permission_classes = [IsUserProfile]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action in ["create"]:
            return UserProfileSerializer
        if self.action in ["validate_user_create"]:
            return UserCreateSerializer
        return self.serializer_class

    def create(self, request, *args, **kwargs):
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(
            {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = UserProfileSerializer(
            instance,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(
            {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = UserProfileSerializer(instance)
        return Response(serializer.data)

    @action(
        detail=False,
        methods=["post"],
        permission_classes=[permissions.AllowAny],
        url_path="validate-user-create",
    )
    def validate_user_create(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            return Response({"success": True})
        return Response(
            {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )

    @action(
        detail=False,
        methods=["get"],
        url_path="me",
    )
    def me(self, request):
        get_object_or_404(UserProfile, user=request.user)

        serializer = UserProfileSerializer(request.user.profile)
        return Response(serializer.data)


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom TokenObtainPairView to add user data to the token payload.
    """

    serializer_class = CustomTokenObtainPairSerializer

    def set_cookie(self, response, key, value):
        response.set_cookie(
            key=key,
            value=value,
            httponly=False,
            domain=".localhost:8000",
        )
