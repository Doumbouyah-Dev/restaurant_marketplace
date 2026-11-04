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