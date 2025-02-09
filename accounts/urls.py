from django.urls import path
from accounts.views import (
    UserRegistrationView,
    UserLoginView,
    EmailConfirmationView,
    CustomPasswordResetView,
    CustomPasswordResetConfirmView,
    CustomPasswordResetCompleteView,
    CustomPasswordResetDoneView,
)

app_name = "accounts"

urlpatterns = [
    path("login/", UserLoginView.as_view(), name="login"),
    path("register/", UserRegistrationView.as_view(), name="register"),
    path(
        "email_confirm/<uidb64>/<token>/",
        EmailConfirmationView.as_view(),
        name="email_confirm",
    ),
    path("reset-password/", CustomPasswordResetView.as_view(), name="password_reset"),
    path(
        "reset-password/done/",
        CustomPasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset-password/confirm/<uidb64>/<token>/",
        CustomPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset-password/complete/",
        CustomPasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
]
