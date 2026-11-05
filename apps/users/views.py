from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .serializers import (
    CustomTokenObtainPairSerializer,
    CustomTokenRefreshSerializer, 
    UserRegistrationSerializer,
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
    

class UserRegistrationView(generics.CreateAPIView):
    """
    API endpoint for creating a new Bistro West customer account.
    """

    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]