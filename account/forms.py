"""Forms for the accounts apps."""

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import ScorchUser


class ScorchUserCreationForm(UserCreationForm):

    class Meta:
        model = ScorchUser
        fields = ("username", "first_name", "last_name", "email")


class ScorchUserChangeForm(UserChangeForm):

    class Meta:
        model = ScorchUser
        fields = ("username", "first_name", "last_name", "email")
