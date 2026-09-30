from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class AdminPanelTests(APITestCase):
    def setUp(self):
        self.staff = User.objects.create_user(username="admin1", password="StrongPass123", is_staff=True)
        self.plain = User.objects.create_user(username="user1", password="StrongPass123")

    def _login(self, username):
        resp = self.client.post(reverse("login"), {"username": username, "password": "StrongPass123"})
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {resp.data['access']}")

    def test_non_staff_forbidden(self):
        self._login("user1")
        resp = self.client.get(reverse("admin-users"))
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_staff_can_list_users(self):
        self._login("admin1")
        resp = self.client.get(reverse("admin-users"))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(resp.data), 2)
