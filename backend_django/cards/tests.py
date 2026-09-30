from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Card


class CardTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="erin", password="StrongPass123")
        login = self.client.post(reverse("login"), {"username": "erin", "password": "StrongPass123"})
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {login.data['access']}")

    def test_add_card_does_not_store_full_number(self):
        resp = self.client.post(
            reverse("card-list-create"),
            {
                "card_holder_name": "Erin Smith",
                "brand": "VISA",
                "expiry_month": 12,
                "expiry_year": 2030,
                "card_number": "4111111111111234",
            },
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        card = Card.objects.get()
        self.assertEqual(card.last4, "1234")
        self.assertEqual(card.masked_number, "**** **** **** 1234")
        self.assertNotIn("card_number", resp.data)

    def test_list_cards_only_returns_own_cards(self):
        other = User.objects.create_user(username="frank", password="StrongPass123")
        Card.objects.create(
            user=other, card_holder_name="Frank", brand="VISA", last4="9999",
            masked_number="**** **** **** 9999", expiry_month=1, expiry_year=2028,
        )
        resp = self.client.get(reverse("card-list-create"))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 0)

    def test_delete_card(self):
        card = Card.objects.create(
            user=self.user, card_holder_name="Erin", brand="VISA", last4="1111",
            masked_number="**** **** **** 1111", expiry_month=1, expiry_year=2028,
        )
        resp = self.client.delete(reverse("card-delete", args=[card.id]))
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Card.objects.filter(id=card.id).exists())
