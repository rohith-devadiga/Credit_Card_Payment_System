from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class AuthTests(APITestCase):
    def test_register(self):
        resp = self.client.post(
            reverse("register"),
            {"username": "alice", "email": "alice@example.com", "password": "StrongPass123"},
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="alice").exists())

    def test_register_password_is_hashed(self):
        self.client.post(
            reverse("register"),
            {"username": "bob", "email": "bob@example.com", "password": "StrongPass123"},
        )
        user = User.objects.get(username="bob")
        self.assertNotEqual(user.password, "StrongPass123")

    def test_login_success(self):
        User.objects.create_user(username="carol", password="StrongPass123")
        resp = self.client.post(reverse("login"), {"username": "carol", "password": "StrongPass123"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn("access", resp.data)
        self.assertIn("refresh", resp.data)

    def test_login_failure(self):
        resp = self.client.post(reverse("login"), {"username": "nouser", "password": "wrong"})
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_protected_route_requires_auth(self):
        resp = self.client.get(reverse("me"))
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_protected_route_with_token(self):
        User.objects.create_user(username="dave", password="StrongPass123")
        login_resp = self.client.post(reverse("login"), {"username": "dave", "password": "StrongPass123"})
        token = login_resp.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        resp = self.client.get(reverse("me"))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data["username"], "dave")
