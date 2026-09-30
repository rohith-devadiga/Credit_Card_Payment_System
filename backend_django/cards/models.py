from django.contrib.auth.models import User
from django.db import models


class Card(models.Model):
    """
    Stores only a masked representation of a card. The real PAN and CVV
    are never persisted -- only the brand, last 4 digits, expiry and a
    masked display string (e.g. '**** **** **** 1234') are kept.
    """

    BRAND_CHOICES = [
        ("VISA", "Visa"),
        ("MASTERCARD", "Mastercard"),
        ("AMEX", "American Express"),
        ("OTHER", "Other"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cards")
    card_holder_name = models.CharField(max_length=120)
    brand = models.CharField(max_length=20, choices=BRAND_CHOICES, default="OTHER")
    last4 = models.CharField(max_length=4)
    masked_number = models.CharField(max_length=25)
    expiry_month = models.PositiveSmallIntegerField()
    expiry_year = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.brand} {self.masked_number} ({self.user.username})"
