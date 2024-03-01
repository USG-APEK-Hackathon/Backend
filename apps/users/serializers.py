from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.users.models import User, UserProfile


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom TokenObtainPairSerializer to add user data to the token payload.
    """

    def get_token(self, user):
        token = super().get_token(user)
        self.add_user_data_to_token(token, user)
        return token

    def add_user_data_to_token(self, token, user):
        token["user_id"] = user.id
        if hasattr(user, "profile") and user.profile:
            token["profile_id"] = user.profile.id
            token["first_name"] = user.first_name
            token["last_name"] = user.last_name
            token["profile_image"] = user.profile.profile_image_url

    def validate(self, attrs):
        username_input = attrs.get("username")
        password_input = attrs.get("password")

        if not username_input or not password_input:
            raise serializers.ValidationError(
                "Must include 'username' and 'password'."
            )

        user = self.authenticate_user(username_input, password_input)

        if user is None:
            raise serializers.ValidationError(
                {
                    "authentication": "User with this username and password "
                    "combination does not exist."
                }
            )

        data = super().validate(attrs)
        self.add_user_data_to_data(data, user)
        return data

    def authenticate_user(self, username, password):
        return authenticate(
            request=self.context.get("request"),
            username=username,
            password=password,
        )

    def add_user_data_to_data(self, data, user):
        data["user_id"] = user.id
        if hasattr(user, "profile") and user.profile:
            data["profile_id"] = user.profile.id
            data["first_name"] = user.first_name
            data["last_name"] = user.last_name
            data["profile_image"] = user.profile.profile_image_url

    class Meta:
        model = User
        fields = ("id", "username", "password")


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer for User model."""

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "password",
            "email",
            "first_name",
            "last_name",
        )
        extra_kwargs = {"password": {"write_only": True}}

    def validate_password(self, value):
        try:
            validate_password(value)
        except DjangoValidationError as exc:
            raise serializers.ValidationError(str(exc))
        return value

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])

        user = User.objects.create(**validated_data)

        return user


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for UserProfile model."""

    user = UserCreateSerializer()

    class Meta:
        model = UserProfile
        fields = [
            "id",
            "birth_date",
            "profile_image",
            "user",
        ]

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user = UserCreateSerializer().create(user_data)
        profile = UserProfile.objects.create(user=user, **validated_data)

        return profile

    def update(self, instance, validated_data):
        instance.birth_date = validated_data.get(
            "birth_date",
            instance.birth_date,
        )
        instance.profile_image = validated_data.get(
            "profile_image", instance.profile_image
        )

        user_data = validated_data.get("user")
        if user_data:
            user_serializer = UserCreateSerializer()
            user = user_serializer.update(instance.user, user_data)
            instance.user = user

        instance.save()
        return instance
