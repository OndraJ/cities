from django.test import TestCase
from django.urls import reverse

from accounts.models import User


class UserRegistrationTestCase(TestCase):
    def test_registration(self):
        response = self.client.post(reverse('register'), {
            'username': 'testuser',
            'email': 'testuser@test.com',
            'password1': 'testpassword',
            'password2': 'testpassword'
        })
        self.assertEqual(response.status_code, 302)

        user = User.objects.get(email='testuser@test.com')
        self.assertEqual(user.username, 'testuser')