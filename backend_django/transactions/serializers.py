from rest_framework import serializers

from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    card_last4 = serializers.CharField(source="card.last4", read_only=True, default=None)

    class Meta:
        model = Transaction
        fields = [
            "id", "reference_id", "amount", "currency", "status",
            "failure_reason", "card_last4", "created_at", "updated_at",
        ]
        read_only_fields = fields
