import csv

from django.http import HttpResponse
from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.views import APIView

from .models import Transaction
from .serializers import TransactionSerializer


class TransactionListView(generics.ListAPIView):
    """
    GET /api/transactions/?status=SUCCESS&date_from=2026-01-01&date_to=2026-01-31&min_amount=10&max_amount=500
    Lists the current user's transactions, filterable by date range,
    amount range and status.
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TransactionSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ["created_at", "amount"]

    def get_queryset(self):
        qs = Transaction.objects.filter(user=self.request.user)
        params = self.request.query_params
        status_param = params.get("status")
        date_from = params.get("date_from")
        date_to = params.get("date_to")
        min_amount = params.get("min_amount")
        max_amount = params.get("max_amount")

        if status_param:
            qs = qs.filter(status=status_param.upper())
        if date_from:
            qs = qs.filter(created_at__date__gte=date_from)
        if date_to:
            qs = qs.filter(created_at__date__lte=date_to)
        if min_amount:
            qs = qs.filter(amount__gte=min_amount)
        if max_amount:
            qs = qs.filter(amount__lte=max_amount)
        return qs


class TransactionExportView(APIView):
    """GET /api/transactions/export/ -- admin-only CSV export of all transactions."""

    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="transactions.csv"'
        writer = csv.writer(response)
        writer.writerow(["reference_id", "user", "amount", "currency", "status", "created_at"])
        for t in Transaction.objects.select_related("user").all():
            writer.writerow([t.reference_id, t.user.username, t.amount, t.currency, t.status, t.created_at])
        return response
