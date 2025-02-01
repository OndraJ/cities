from django.urls import path

from accounts.views import UserRegistrationView, UserLoginView

app_name = "accounts"

urlpatterns = [
    path("", UserLoginView.as_view(), name="login"),
    path("register/", UserRegistrationView.as_view(), name="register"),
]
