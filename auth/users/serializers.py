from django.contrib.auth import get_user_model

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
        user = User.objects.update_user(instance, **validated_data)
        return user

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
