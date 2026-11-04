from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .serializers import (
    CustomTokenObtainPairSerializer,
    CustomTokenRefreshSerializer,
)


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Login endpoint for Bistro West.
    """
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [AllowAny]


class CustomTokenRefreshView(TokenRefreshView):
    """
    Refresh endpoint for Bistro West.
    """
    serializer_class = CustomTokenRefreshSerializer
    permission_classes = [AllowAny]