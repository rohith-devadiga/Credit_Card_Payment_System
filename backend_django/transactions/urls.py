from django.urls import path

from .views import TransactionExportView, TransactionListView

urlpatterns = [
    path("", TransactionListView.as_view(), name="transaction-list"),
    path("export/", TransactionExportView.as_view(), name="transaction-export"),
]
