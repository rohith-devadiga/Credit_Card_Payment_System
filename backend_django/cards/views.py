from rest_framework import generics, permissions

from .models import Card
from .serializers import CardCreateSerializer, CardSerializer


class CardListCreateView(generics.ListCreateAPIView):
    """GET: list the current user's saved cards. POST: add a new card."""

    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Card.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        return CardCreateSerializer if self.request.method == "POST" else CardSerializer


class CardDeleteView(generics.DestroyAPIView):
    """DELETE /api/cards/<id>/ -- remove a saved card."""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CardSerializer

    def get_queryset(self):
        return Card.objects.filter(user=self.request.user)
