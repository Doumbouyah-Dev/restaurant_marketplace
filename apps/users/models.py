
import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):

    class Role(models.TextChoices):
        CUSTOMER = "CUSTOMER", "Customer"
        VENDOR = "VENDOR", "Vendor"
        ADMIN = "ADMIN", "Administrator"

    # Primary identifier
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    # Authentication and public identity
    email = models.EmailField(
        max_length=254,
        unique=True
    )

    username = models.CharField(
        max_length=150,
        unique=True
    )

    # Account role
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.CUSTOMER
    )

    # Verification status
    is_verified = models.BooleanField(
        default=False
    )

    # Django account permissions
    is_active = models.BooleanField(
        default=True
    )

    is_staff = models.BooleanField(
        default=False
    )

    # Account creation timestamp
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    # Custom manager
    objects = CustomUserManager()

    # Email-based authentication
    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = ["username"]

    class Meta:
        db_table = "users_customuser"
        ordering = ["-created_at"]
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return f"{self.email} ({self.role})"
