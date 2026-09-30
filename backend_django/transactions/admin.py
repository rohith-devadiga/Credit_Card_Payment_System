from django.contrib import admin

from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("reference_id", "user", "amount", "currency", "status", "created_at")
    list_filter = ("status", "currency")
    search_fields = ("reference_id", "user__username")
