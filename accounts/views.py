from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import FormView

from accounts.forms import CustomUserCreationForm


class UserRegistrationView(FormView):
    template_name = "accounts/register.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("accounts:login")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class UserLoginView(LoginView):
    template_name = "accounts/login.html"
    form_class = AuthenticationForm

    def get_success_url(self):
        return reverse_lazy("core:home")
