from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from mailing.models import NULLABLE


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name=_("email"))

    name = models.CharField(max_length=64, verbose_name=_("name"))
    surname = models.CharField(max_length=64, verbose_name=_("surname"))
    avatar = models.ImageField(upload_to="users/avatars/", **NULLABLE, verbose_name=_("avatar"))
    token = models.CharField(max_length=32, verbose_name=_("token"), **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        permissions = [
            ("change_active", "Can change is_active"),
        ]

    def __str__(self):
        return self.email
