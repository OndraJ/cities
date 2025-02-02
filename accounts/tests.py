from django.test import TestCase
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from accounts.models import User
from accounts.helpers import TokenGenerator


class UserRegistrationTestCase(TestCase):
    def test_user_registration_ok(self):
        response = self.client.post(
            reverse("accounts:register"),
            {
                "username": "testuser",
                "email": "testuser@test.com",
                "password1": "testpassword",
                "password2": "testpassword",
            },
        )
        self.assertEqual(response.status_code, 302)

        user = User.objects.get(email="testuser@test.com")
        self.assertEqual(user.username, "testuser")

    def test_cannot_register_user_with_existing_email(self):
        User.objects.create_user("testuser", "testuser@test.com", "testpassword")
        users = User.objects.all()

        self.assertEqual(users.count(), 1)

        response = self.client.post(
            reverse("accounts:register"),
            {
                "username": "testuser2",
                "email": "testuser@test.com",
                "password1": "testpassword",
                "password2": "testpassword",
            },
        )
        self.assertContains(
            response, "User with this Email already exists.", status_code=200
        )

        users = User.objects.all()
        self.assertEqual(users.count(), 1)

    def test_user_can_login(self):
        email = "testuser@test.com"
        password = "testpassword"
        User.objects.create_user("testuser", email, password)
        # TODO: Try to figure out how to use "email" instead of "username" to login,
        # as I have set the USERNAME_FIELD to "email" in the User model
        response = self.client.post(
            reverse("accounts:login"),
            {"username": email, "password": password},
        )
        self.assertEqual(response.status_code, 302)
        self.assertContains(self.client.get(response.url), "Hello World")


class EmailConfirmationTestCase(TestCase):
    def test_email_confirmation(self):
        email = "testemail@email.com"
        self.client.post(
            reverse("accounts:register"),
            {
                "username": "testuser",
                "email": email,
                "password1": "testpassword",
                "password2": "testpassword",
            },
        )
        user = User.objects.get(email="testemail@email.com")
        self.assertFalse(user.is_active)

        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = TokenGenerator().make_token(user)
        self.client.get(
            reverse("accounts:email_confirm", kwargs={"uidb64": uidb64, "token": token})
        )
        user.refresh_from_db()
        self.assertTrue(user.is_active)
