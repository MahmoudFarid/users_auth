from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from .factories import UserFactory
from .utils import generate_photo_file

User = get_user_model()


class TestUserViewSet(APITestCase):
    def setUp(self):
        self.unauthorized_client = APIClient()

        self.user = UserFactory.create()
        self.authorized_client = APIClient()
        token, _ = Token.objects.get_or_create(user=self.user)
        self.authorized_client.credentials(HTTP_AUTHORIZATION="Token " + token.key)

        self.api = "/api/v1/users/"

        self.data = {
            "username": "mahmoud_farid",
            "first_name": "Mahmoud",
            "last_name": "Farid",
            "avatar": generate_photo_file(),
            "password": "someComplexPass123",
        }

    def test_create_user(self):
        users_count = User.objects.count()

        response = self.unauthorized_client.post(
            self.api, data=self.data, format="multipart"
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.count(), users_count + 1)
        response = response.json()
        user = User.objects.last()
        self.assertTrue(user.is_active)
        self.assertNotEqual(user.password, self.data.get("password"))
        self.assertTrue(user.check_password(self.data.get("password")))
        self.assertEqual(response.get("username"), self.data.get("username"))
        self.assertEqual(response.get("first_nme"), self.data.get("first_nme"))
        self.assertEqual(response.get("last_name"), self.data.get("last_name"))
        self.assertIsNotNone(response.get("avatar"))

    def test_create_user_with_empty_data(self):
        users_count = User.objects.count()
        data = {}
        response = self.unauthorized_client.post(
            self.api, data=data, format="multipart"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(User.objects.count(), users_count)
        response = response.json()
        self.assertEqual(len(response.keys()), 2)
        self.assertEqual(response.get("username"), ["This field is required."])
        self.assertEqual(response.get("password"), ["This field is required."])

    def test_create_user_with_duplicate_username(self):
        UserFactory(username=self.data.get("username"))
        users_count = User.objects.count()

        response = self.unauthorized_client.post(
            self.api, data=self.data, format="multipart"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(User.objects.count(), users_count)
        response = response.json()
        self.assertEqual(
            response.get("username"), ["user with this username already exists."]
        )

    def test_list_users(self):
        UserFactory.create_batch(5)
        response = self.unauthorized_client.get(self.api)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 6)
        response = response.json()
        for result in response.get("results"):
            user = User.objects.get(username=result["username"])
            self.assertEqual(result.get("first_name"), user.first_name)
            self.assertEqual(result.get("last_name"), user.last_name)
            self.assertIn(user.get_absolute_url(), result.get("url"))

    def test_retrieve_user_by_username(self):
        response = self.unauthorized_client.get(
            "{}{}/".format(self.api, self.user.username),
        )
        self.assertEqual(response.status_code, 200)
        response = response.json()
        user = User.objects.get(username=response["username"])
        self.assertEqual(response.get("first_name"), user.first_name)
        self.assertEqual(response.get("last_name"), user.last_name)
        self.assertIn(user.get_absolute_url(), response.get("url"))

    def test_update_user_profile_info(self):
        data = {
            "username": "updated_username",
            "first_name": "Updated",
            "last_name": "Name",
            "avatar": generate_photo_file(),
            "password": "UpdatePassword",
        }
        response = self.authorized_client.put(
            "{}{}/".format(self.api, self.user.username),
            data=data,
            format="multipart",
        )
        self.assertEqual(response.status_code, 200)
        response = response.json()
        self.user.refresh_from_db()
        self.assertNotEqual(self.user.password, data.get("password"))
        self.assertTrue(self.user.check_password(data.get("password")))
        self.assertEqual(response.get("username"), data.get("username"))
        self.assertEqual(response.get("first_nme"), data.get("first_nme"))
        self.assertEqual(response.get("last_name"), data.get("last_name"))
        self.assertIsNotNone(response.get("avatar"))

    def test_update_another_user_profile(self):
        user = UserFactory.create()
        data = {
            "username": "updated_username",
            "first_name": "Updated",
            "last_name": "Name",
            "avatar": generate_photo_file(),
            "password": "UpdatePassword",
        }
        response = self.authorized_client.put(
            "{}{}/".format(self.api, user.username),
            data=data,
            format="multipart",
        )
        self.assertEqual(response.status_code, 403)

    def test_delete_user(self):
        self.assertEqual(User.objects.count(), 1)

        response = self.authorized_client.delete(
            "{}{}/".format(self.api, self.user.username),
        )
        self.assertEqual(response.status_code, 204)
        self.assertEqual(User.objects.count(), 0)

    def test_delete_another_user(self):
        user = UserFactory.create()
        self.assertEqual(User.objects.count(), 2)

        response = self.authorized_client.delete(
            "{}{}/".format(self.api, user.username),
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(User.objects.count(), 2)
