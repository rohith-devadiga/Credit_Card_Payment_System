from rest_framework import serializers

from .models import Card


class CardCreateSerializer(serializers.ModelSerializer):
    """
    Accepts a full card number as write-only input so it never appears
    in a response or gets stored -- only last4 + a masked string are
    derived from it and saved.
    """

    card_number = serializers.CharField(write_only=True, min_length=12, max_length=19)

    class Meta:
        model = Card
        fields = ["id", "card_holder_name", "brand", "expiry_month", "expiry_year", "card_number", "last4", "masked_number", "created_at"]
        read_only_fields = ["last4", "masked_number", "created_at"]

    def validate_card_number(self, value):
        digits = value.replace(" ", "")
        if not digits.isdigit():
            raise serializers.ValidationError("Card number must contain only digits.")
        return digits

    def create(self, validated_data):
        number = validated_data.pop("card_number")
        last4 = number[-4:]
        masked = "**** **** **** " + last4
        validated_data["last4"] = last4
        validated_data["masked_number"] = masked
        validated_data["user"] = self.context["request"].user
        return Card.objects.create(**validated_data)


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ["id", "card_holder_name", "brand", "masked_number", "last4", "expiry_month", "expiry_year", "created_at"]
