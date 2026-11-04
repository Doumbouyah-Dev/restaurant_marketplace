from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Admin configuration for Bistro West custom users.
    """

    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    list_display = (
        "email",
        "username",
        "role",
        "is_verified",
        "is_active",
        "is_staff",
    )

    list_filter = (
        "role",
        "is_verified",
        "is_active",
        "is_staff",
        "is_superuser",
    )

    search_fields = ("email", "username")

    ordering = ("email",)

    readonly_fields = ("last_login", "created_at")

    filter_horizontal = ("groups", "user_permissions")

    fieldsets = (
        ("Account Information", {
            "fields": ("email", "username", "password")
        }),
        ("Profile", {
            "fields": ("role", "is_verified")
        }),
        ("Permissions", {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            )
        }),
        ("Important Dates", {
            "fields": ("last_login", "created_at")
        }),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email",
                "username",
                "role",
                "password1",
                "password2",
            ),
        }),
    )