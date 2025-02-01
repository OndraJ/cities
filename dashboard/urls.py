from django.urls import path

from dashboard.views import HomeView

app_name = "dashboard"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
]
