import uuid

from django.contrib.auth.models import User
from django.db import models

from cards.models import Card


class Transaction(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("SUCCESS", "Success"),
        ("FAILED", "Failed"),
    ]

    reference_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transactions")
    card = models.ForeignKey(Card, on_delete=models.SET_NULL, null=True, related_name="transactions")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default="USD")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="PENDING")
    failure_reason = models.CharField(max_length=255, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.reference_id} - {self.amount} {self.currency} - {self.status}"
