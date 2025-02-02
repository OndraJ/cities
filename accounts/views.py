from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.views.generic import FormView

from accounts.forms import CustomUserCreationForm
from accounts.helpers import TokenGenerator, confirm_email
from accounts.models import User


class UserRegistrationView(FormView):
    template_name = "accounts/register.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("accounts:login")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        messages.success(
            self.request,
            f"Dear {form.cleaned_data.get("username")}, \n"
            f"Please confirm your email address: {form.cleaned_data.get("email")} to activate your account. \n",
        )
        confirm_email(self.request, user)
        return super().form_valid(form)


class UserLoginView(LoginView):
    template_name = "accounts/login.html"
    form_class = AuthenticationForm

    def get_success_url(self):
        return reverse_lazy("dashboard:home")


class EmailConfirmationView(View):
    success_url = reverse_lazy("accounts:login")

    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and TokenGenerator().check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(
                self.request, "Your email has been confirmed. You can now login."
            )
            return redirect(self.success_url)
        else:
            messages.error(
                self.request, "The confirmation link is invalid or has expired."
            )
            return redirect(reverse("accounts:register"))
