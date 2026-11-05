from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    """
    Manager for creating and managing Bistro West users.

    Users authenticate using their email address.
    """

    def create_user(self, email, username, secret=None, role="CUSTOMER", **extra_fields):
        if not email:
            raise ValueError("An email address is required.")

        if not username:
            raise ValueError("A username is required.")

        if not secret:
            raise ValueError("A secret is required.")

        email = self.normalize_email(email).lower()
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_verified", False)

        user = self.model(
            email=email,
            username=username,
            role=role,
            **extra_fields,
        )
        user.set_password(secret)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, secret=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_verified", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        extra_fields.setdefault("role", "ADMIN")

        if extra_fields["role"] != "ADMIN":
            raise ValueError("Superuser must have the ADMIN role.")

        return self.create_user(
            email=email,
            username=username,
            secret=secret,
            **extra_fields,
        )