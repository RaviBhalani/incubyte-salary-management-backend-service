from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.settings import api_settings
from rest_framework import exceptions, serializers, status
from rest_framework.serializers import ModelSerializer
from django.core.validators import validate_email
from apps.user.models import User
from apps.user.utils import get_tokens_for_user

from apps.user.constants import (
    EMAIL_REQUIRED,
    USER_DOES_NOT_EXIST,
    NO_ACTIVE_ACCOUNT_FOUND,

)


class TokenObtainPairSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, validators=[validate_email])
    password = serializers.CharField()

    def validate(self, data):

        try:
            user = User.objects.get(email=data["email"])
        except User.DoesNotExist:
            raise serializers.ValidationError(
                USER_DOES_NOT_EXIST
            )

        valid = user.check_password(data["password"])
        if valid:
            data = get_tokens_for_user(user)
            if api_settings.UPDATE_LAST_LOGIN:
                update_last_login(None, user)
        else:
            raise serializers.ValidationError(
                NO_ACTIVE_ACCOUNT_FOUND,
            )
        return data


class UserListSerializer(ModelSerializer):
    """
    serializer to list users
    """
    
    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "middle_name",
            "last_name",
            "email",
            
        )


class UserSerializer(ModelSerializer):
    """
    Serializer for Role Model
    """
    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):
        """
        custom create method override for user post request
        """
        
        user = User.objects.create(**validated_data)
        
        user.save()
        return user

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep.update(instance.to_representation())
        return rep



