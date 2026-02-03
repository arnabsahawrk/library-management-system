from uuid import uuid4
from django.db import models
from django.contrib.auth.models import AbstractUser

from accounts.managers import CustomUserManager


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    username = None
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects: CustomUserManager = CustomUserManager()

    def __str__(self):
        return self.email
