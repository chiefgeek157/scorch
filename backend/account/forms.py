"""Forms for the accounts apps."""

from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import Account


class AccountCreationForm(UserCreationForm):

    class Meta:
        model = Account
        fields = ("username", "first_name", "last_name", "email")


class AccountChangeForm(UserChangeForm):

    class Meta:
        model = Account
        fields = ("username", "first_name", "last_name", "email")
