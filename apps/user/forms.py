from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from apps.user.constants import PASSWORDS_DO_NOT_MATCH
from apps.user.models import User


class UserDetailsCreationForm(UserCreationForm):
    """
    Custom creation form for User details
    """

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name")

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(PASSWORDS_DO_NOT_MATCH)
        return password2

    def save(self, commit=True):
        user = super(UserDetailsCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserDetailsChangeForm(UserChangeForm):
    """
    Custom change form for User details
    """

    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "password",
            "is_active",
            "is_staff",
            "is_superuser",
            "groups",
            "user_permissions",
        )
