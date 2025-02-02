from django.urls import path

from accounts.views import UserRegistrationView, UserLoginView, EmailConfirmationView

app_name = "accounts"

urlpatterns = [
    path("", UserLoginView.as_view(), name="login"),
    path("register/", UserRegistrationView.as_view(), name="register"),
    path(
        "email_confirm/<uidb64>/<token>/",
        EmailConfirmationView.as_view(),
        name="email_confirm",
    ),
]
