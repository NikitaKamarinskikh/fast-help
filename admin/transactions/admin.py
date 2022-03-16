from django.contrib import admin
from .models import Transactions, Withdrawals


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


@admin.register(Withdrawals)
class WithdrawalsAdmin(admin.ModelAdmin):
    search_fields = [
        "bot_user__telegram_id",
        "pk",
    ]

    list_display = ["user", "created_at", "coins_before", "coins", "coins_after"]

    class Meta:
        model = Withdrawals



