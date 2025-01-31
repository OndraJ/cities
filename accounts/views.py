from django.contrib.auth import login
from django.shortcuts import render
from django.views.generic import FormView

from accounts.forms import CustomUserCreationForm


class UserRegistrationView(FormView):
    template_name = 'accounts/register.html'
    form_class = CustomUserCreationForm
    success_url = '/'

    def form_valid(self, form):
        form.save()
        login(self.request, form.instance)
        return super().form_valid(form)