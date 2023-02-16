from django.shortcuts import render

from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .forms import ScorchUserCreationForm

class RegisterView(CreateView):
    form_class = ScorchUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/register.html"
