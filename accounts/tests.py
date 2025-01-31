from django.test import TestCase
from django.urls import reverse

from accounts.models import User


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
