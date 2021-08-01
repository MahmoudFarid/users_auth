import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .managers import UserInheritanceManager, UserManager


def user_avatar_path(instance, filename):
    ext = filename.split(".")[-1]
    filename = "{}.{}".format(uuid.uuid4(), ext)

    return "avatars/{}".format(filename)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_("username"), max_length=150, unique=True)
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    avatar = models.ImageField(_("Avatar"), upload_to=user_avatar_path, blank=True)

    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    objects = UserInheritanceManager()
    base_objects = UserManager()

    USERNAME_FIELD = "username"

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("api:rest_users:user-detail", kwargs={"username": self.username})
