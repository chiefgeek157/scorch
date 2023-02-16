from django.contrib import admin

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import ScorchUserCreationForm, ScorchUserChangeForm
from .models import ScorchUser

class ScorchUserAdmin(UserAdmin):
    add_form = ScorchUserCreationForm
    form = ScorchUserChangeForm
    model = ScorchUser
    list_display = ["email", "first_name", "last_name", "username",]

admin.site.register(ScorchUser, ScorchUserAdmin)
