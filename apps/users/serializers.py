from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Authenticate Bistro West users using email and password.
    """
    username_field = "email"


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    """
    Validate refresh tokens and issue rotated tokens.
    """
    pass

# =========================================
# 
# =========================================

from rest_framework import serializers

from .models import CustomUser


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for registering a new Bistro West customer.
    """

    password = serializers.CharField(
        write_only=True,
        min_length=8
    )

    password_confirm = serializers.CharField(
        write_only=True
    )

    class Meta:
        model = CustomUser
        fields = (
            "email",
            "username",
            "password",
            "password_confirm",
        )

    def validate_email(self, value):
        """
        Normalize the email and prevent duplicate accounts.
        """
        value = value.lower().strip()

        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "A user with this email address already exists."
            )

        return value

    def validate_username(self, value):
        """
        Prevent duplicate usernames.
        """
        value = value.strip()

        if CustomUser.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                "A user with this username already exists."
            )

        return value

    def validate(self, attrs):
        """
        Make sure both password fields match.
        """
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError({
                "password_confirm": "Passwords do not match."
            })

        return attrs

    def create(self, validated_data):
        """
        Create the user through the custom user manager
        so the password is securely hashed.
        """
        validated_data.pop("password_confirm")

        password = validated_data.pop("password")

        user = CustomUser.objects.create_user(
            secret=password,
            role=CustomUser.Role.CUSTOMER,
            **validated_data
        )

        return user