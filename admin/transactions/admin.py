from django.contrib import admin
from .models import Transactions


@admin.register(Transactions)
class TransactionsAdmin(admin.ModelAdmin):
    search_fields = [
        "created_at",
        "bot_user__telegram_id",
        "pk",
    ]

    list_display = ["bot_user", "created_at", "amount", "is_paid"]

    class Meta:
        model = Transactions


