from django.contrib.auth.forms import UserCreationForm
from django import forms

from accounts.models import User


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.help_text = None

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
