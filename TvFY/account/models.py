from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models

from TvFY.core.helpers import UnicodeUsernameValidator


class AccountManager(models.Manager):
    def get_by_natural_key(self, username):
        return self.get(**{self.model.USERNAME_FIELD: username})


class Account(AbstractBaseUser):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        unique=True,
        max_length=50,
        validators=[username_validator],
    )
    email = models.CharField(max_length=100)

    USERNAME_FIELD = "username"

    objects = AccountManager()
