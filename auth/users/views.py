from django.contrib.auth import get_user_model

from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from .permissions import CurrentUserPermission
from .serializers import UserCreateSerializer, UserSerializer

User = get_user_model()


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    lookup_field = "username"

    def get_serializer_class(self):
        if self.action in ["create", "update"]:
            return UserCreateSerializer
        return self.serializer_class

    def get_permissions(self):
        if self.action in ["update", "delete", "destroy"]:
            self.permission_classes = [CurrentUserPermission]
        return super().get_permissions()
