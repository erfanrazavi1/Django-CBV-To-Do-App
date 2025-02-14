from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import ValidationError


# Serializer for user registration, including password validation and creation
class CustomRegistrationSerializer(serializers.ModelSerializer):
    """
    This serializer handles user registration
    It validates the user's passwords, checks if they match,
    and ensures the password meets required criteria.
    It also creates a user after validation.
    """

    password = serializers.CharField(required=True, write_only=True)
    password1 = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ["username", "password", "password1"]

    def validate(self, attrs):
        """
        Validates that both passwords match and that
        the password meets Django's security requirements.
        """
        if attrs["password"] != attrs["password1"]:
            raise serializers.ValidationError({"detail": "Passwords do not match"})
        try:
            # Validate password strength
            validate_password(attrs.get("password"))
        except ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})
        return super().validate(attrs)

    def create(self, validated_data):
        """
        Creates a new user with the validated data,
        excluding the 'password1' field.
        """
        validated_data.pop("password1", None)
        user = User.objects.create_user(**validated_data)
        return user


# Serializer for changing the user's password
class ChangePasswordSerializer(serializers.Serializer):
    """
    This serializer handles the password
    change process for an authenticated user.
    It validates that the old password is correct and ensures
    the new passwords match and meet the required criteria.
    """

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password1 = serializers.CharField(required=True)

    def validate(self, attrs):
        """
        Validates that the new passwords match
        and checks the new password's strength.
        """
        if attrs.get("new_password") != attrs.get("new_password1"):
            raise serializers.ValidationError({"detail": "Passwords do not match"})
        try:
            # Validate the new password strength
            validate_password(attrs.get("new_password"))
        except ValidationError as e:
            raise serializers.ValidationError({"new_password": list(e.messages)})
        return super().validate(attrs)


# Serializer for resetting the user's password by email
class ResetPasswordSerializer(serializers.Serializer):
    """
    This serializer handles the email input for requesting a password reset
    It ensures the email format is valid.
    """

    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        """
        Validates that the email is provided and in the correct format.
        """
        email = attrs.get("email")
        if not email:
            raise serializers.ValidationError({"email": "This field is required."})
        return attrs


# Serializer for confirming the password reset by setting a new password
class ResetPasswordConfirmSerializer(serializers.Serializer):
    """
    This serializer validates the new password input
    for the reset password process.
    It checks if both new passwords match and validates
    that the new password meets the required strength.
    """

    new_password = serializers.CharField(write_only=True, required=True)
    new_password1 = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        """
        Validates that the new passwords match
        and checks the strength of the new password.
        """
        if attrs.get("new_password") != attrs.get("new_password1"):
            raise serializers.ValidationError({"detail": "Passwords do not match"})
        try:
            # Validate the strength of the new password
            validate_password(attrs.get("new_password"))
        except ValidationError as e:
            raise serializers.ValidationError({"new_password": list(e.messages)})
        return attrs
