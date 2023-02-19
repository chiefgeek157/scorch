from django.contrib.auth.models import AbstractUser
from django.db import models


class Account(AbstractUser):
    """An account in the scorch app."""

    def __str__(self) -> str:
        return self.username
