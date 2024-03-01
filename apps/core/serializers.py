"""Core serializers."""
from rest_framework import serializers


class EmptySerializer(serializers.Serializer):
    """Serializer with no fields
    to handle empty POST, PUT and PATCH requests."""


class ErrorsSerializer(serializers.Serializer):
    """Serializer for error messages."""

    code = serializers.CharField(read_only=True)
    detail = serializers.CharField(read_only=True)
    attr = serializers.CharField(read_only=True)


class ErrorMessageSerializer(serializers.Serializer):
    """Serializer for error messages."""

    type = serializers.CharField(read_only=True)
    errors = ErrorsSerializer(many=True, read_only=True)


class SuccessMessageSerializer(serializers.Serializer):
    """Serializer for success messages."""

    type = serializers.CharField(read_only=True)
    message = serializers.CharField(read_only=True)
    detail = serializers.ListField(read_only=True)
