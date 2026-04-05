from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class UserProfileManager(BaseUserManager):
    """
    User profile manager for User model
    """

    def create_user(self, email=None, password=None):
        # Create a new user
        user = self.model(email=email)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password):
        # Create a new superuser.
        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractUser):
    """
    User details
    """
    username = None
    email = models.EmailField(unique=True)

    objects = UserProfileManager()

    REQUIRED_FIELDS = []
    USERNAME_FIELD = "email"

    class Meta:
        verbose_name_plural = "User details"

    def __str__(self):
        return str(self.first_name)
