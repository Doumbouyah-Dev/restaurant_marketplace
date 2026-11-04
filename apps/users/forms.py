from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """
    Form for creating new Bistro West users in Django Admin.
    """

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("email", "username", "role")


class CustomUserChangeForm(UserChangeForm):
    """
    Form for updating existing Bistro West users in Django Admin.
    """

    class Meta:
        model = CustomUser
        fields = "__all__"
        