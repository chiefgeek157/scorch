from django.contrib.auth.models import AbstractUser
from django.db import models


class ScorchUser(AbstractUser):
    """A user in the scorch app."""

    def __str__(self) -> str:
        return self.username
