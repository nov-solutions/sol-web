from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from user.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = "email"
    objects = UserManager()

    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    # password only applicable to admin users
    password = models.CharField(max_length=255, null=True, blank=True)
    groups = None
    user_permissions = None
