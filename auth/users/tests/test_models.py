from django.contrib.auth import get_user_model
from django.test import TestCase

from .factories import UserFactory

User = get_user_model()


class TestUser(TestCase):
    def test_create_user(self):
        self.assertEqual(User.objects.count(), 0)
        user = UserFactory()
        self.assertEqual(User.objects.count(), 1)
        self.assertIsInstance(user, User)
