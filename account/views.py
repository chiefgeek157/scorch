import logging

from django.contrib.auth.models import Group, User
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .forms import ScorchUserCreationForm

_log = logging.getLogger(__name__)


class RegisterView(CreateView):
    form_class = ScorchUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'

    def post(self, request, *args, **kwargs):
        """Special handling on user registration"""

        form = ScorchUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            _log.info(f'Created user {user}')

            # Add user to default groups
            group = Group.objects.get(name='Viewers')
            user.groups.add(group)
            _log.info(f'Added user {user} to {group}')

            return redirect('login')
        else:
            return render(request, self.template_name, {'form': form})