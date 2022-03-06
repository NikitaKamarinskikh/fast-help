from django.contrib import admin
from .models import Orders, OrderCandidates, OrdersTimestamps


@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ["customer", "category", "worker", "status"]
    search_fields = ["customer_phone", "pk", "customer__user__telegram_id"]

    class Meta:
        model = Orders


@admin.register(OrdersTimestamps)
class OrderTimestampsAdmin(admin.ModelAdmin):
    list_display = ["order", "seconds"]

    class Meta:
        model = OrdersTimestamps

