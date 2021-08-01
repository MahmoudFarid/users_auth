from django.contrib.auth.models import BaseUserManager
from django.utils import timezone

from model_utils.managers import InheritanceQuerySet


class UserManager(BaseUserManager):
    def _create_user(self, username, password, is_staff, is_superuser, **extra_fields):
        now = timezone.now()
        if not username:
            raise ValueError("The given username must be set")

        is_active = extra_fields.pop("is_active", True)
        user = self.model(
            username=username,
            is_staff=is_staff,
            is_active=is_active,
            is_superuser=is_superuser,
            last_login=now,
            **extra_fields
        )
        user.set_password(password)
        user.save()
        return user

    def _update_user(self, user, password, **extra_fields):
        user.set_password(password)
        for field, value in extra_fields.items():
            setattr(user, field, value)
        user.save()
        return user

    def create_user(self, username, password=None, **extra_fields):
        is_staff = extra_fields.pop("is_staff", False)
        return self._create_user(username, password, is_staff, False, **extra_fields)

    def update_user(self, user, password, **extra_fields):
        return self._update_user(user, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        return self._create_user(
            username, password, True, True, is_active=True, **extra_fields
        )


class UserInheritanceManager(UserManager):
    def get_queryset(self):
        return InheritanceQuerySet(self.model).select_subclasses()

    get_query_set = get_queryset
