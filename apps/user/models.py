from apps.core.models import Timestamps
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from apps.user.constants import (
    DEFAULT_NAME_FIELD_MAX_LENGTH,
    PERMISSION_SUB_NAME_MAX_LENGTH,
    PERMISSION_DESCRIPTION_MAX_LENGTH,
    ROLE_NAME_MAX_LENGTH
)

from apps.user.constants import (
    FIRST_NAME_USER_HELP_TEXT,
    MIDDLE_NAME_USER_HELP_TEXT,
    LAST_NAME_USER_HELP_TEXT,
    EMAIL_HELP_TEXT,
    ROLE_HELP_TEXT,
    VERIFIED_HELP_TEXT,
    EMAIL_REQUIRED_MESSAGE,
)


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
    first_name = models.CharField(
        max_length=DEFAULT_NAME_FIELD_MAX_LENGTH,
        help_text=FIRST_NAME_USER_HELP_TEXT
    )
    middle_name = models.CharField(
        max_length=DEFAULT_NAME_FIELD_MAX_LENGTH,
        blank=True,
        null=True,
        help_text=MIDDLE_NAME_USER_HELP_TEXT
    )
    last_name = models.CharField(
        max_length=DEFAULT_NAME_FIELD_MAX_LENGTH,
        help_text=LAST_NAME_USER_HELP_TEXT
    )
    email = models.EmailField(
        unique=True, help_text=EMAIL_HELP_TEXT
    )

    email_verified = models.BooleanField(default=False, help_text=VERIFIED_HELP_TEXT)

    created_ts = models.DateTimeField(auto_now_add=True)
    modified_ts = models.DateTimeField(auto_now=True)

    objects = UserProfileManager()

    REQUIRED_FIELDS = []
    USERNAME_FIELD = "email"

    class Meta:
        verbose_name_plural = "User details"

    def __str__(self):
        return str(self.first_name)

    def to_representation(self):
        rep = {
            "id": self.id,
            "name": self.first_name + self.middle_name + self.last_name,
            "email": self.email,

            "verified": self.email_verified,
            "is_active": self.is_active,
            "is_staff": self.is_staff,
            "is_superuser": self.is_superuser,
            "created_ts": self.created_ts,
            "modified_ts": self.modified_ts,
        }
        return rep

