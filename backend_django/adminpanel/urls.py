from django.urls import path

from .views import AllCardsView, AllTransactionsView, DailySummaryView, UserManagementView

urlpatterns = [
    path("users/", UserManagementView.as_view(), name="admin-users"),
    path("cards/", AllCardsView.as_view(), name="admin-cards"),
    path("transactions/", AllTransactionsView.as_view(), name="admin-transactions"),
    path("summary/", DailySummaryView.as_view(), name="admin-summary"),
]
