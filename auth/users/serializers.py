from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "avatar", "url")

        extra_kwargs = {
            "url": {
                "view_name": "api:rest_users:user-detail",
                "lookup_field": "username",
            }
        }


class UserCreateSerializer(UserSerializer):
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ("password",)

    def update(self, instance, validated_data):
        try:
            user = User.objects.update_user(instance, **validated_data)
        except IntegrityError:
            raise serializers.ValidationError(_("Unable to update user."))
        return user

    def create(self, validated_data):
        try:
            user = User.objects.create_user(**validated_data)
        except IntegrityError:
            raise serializers.ValidationError(_("Unable to create user."))
        return user
