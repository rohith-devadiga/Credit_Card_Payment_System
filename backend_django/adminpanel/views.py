from django.contrib.auth.models import User
from django.db.models import Count, Sum
from django.db.models.functions import TruncDate
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from cards.models import Card
from cards.serializers import CardSerializer
from transactions.models import Transaction
from transactions.serializers import TransactionSerializer

from authentication.serializers import UserSerializer


class IsStaffUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)


class UserManagementView(APIView):
    """GET /api/admin-panel/users/ -- list all users (admin only)."""

    permission_classes = [IsStaffUser]

    def get(self, request):
        return Response(UserSerializer(User.objects.all(), many=True).data)


class AllCardsView(APIView):
    """GET /api/admin-panel/cards/ -- view all saved cards (admin only)."""

    permission_classes = [IsStaffUser]

    def get(self, request):
        return Response(CardSerializer(Card.objects.all(), many=True).data)


class AllTransactionsView(APIView):
    """GET /api/admin-panel/transactions/ -- view all transactions (admin only)."""

    permission_classes = [IsStaffUser]

    def get(self, request):
        return Response(TransactionSerializer(Transaction.objects.all(), many=True).data)


class DailySummaryView(APIView):
    """GET /api/admin-panel/summary/ -- payments grouped by day (admin only)."""

    permission_classes = [IsStaffUser]

    def get(self, request):
        summary = (
            Transaction.objects.annotate(day=TruncDate("created_at"))
            .values("day", "status")
            .annotate(count=Count("id"), total_amount=Sum("amount"))
            .order_by("-day")
        )
        return Response(list(summary))
