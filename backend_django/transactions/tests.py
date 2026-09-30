from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Transaction


class TransactionTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="grace", password="StrongPass123")
        login = self.client.post(reverse("login"), {"username": "grace", "password": "StrongPass123"})
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {login.data['access']}")
        Transaction.objects.create(user=self.user, amount="50.00", status="SUCCESS")
        Transaction.objects.create(user=self.user, amount="20.00", status="FAILED")

    def test_list_transactions(self):
        resp = self.client.get(reverse("transaction-list"))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 2)

    def test_filter_by_status(self):
        resp = self.client.get(reverse("transaction-list"), {"status": "SUCCESS"})
        self.assertEqual(len(resp.data), 1)
        self.assertEqual(resp.data[0]["status"], "SUCCESS")

    def test_export_requires_admin(self):
        resp = self.client.get(reverse("transaction-export"))
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
