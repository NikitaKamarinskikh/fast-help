from django.contrib import admin
from .models import Orders, OrderCandidates


@admin.register(OrderCandidates)
class OrderCandidatesAdmin(admin.ModelAdmin):
    ...


class OrderCandidatesInline(admin.StackedInline):
    model = OrderCandidates
    extra = 0


@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ["customer", "category", "worker", "status"]
    search_fields = ["customer_phone"]
    inlines = [OrderCandidatesInline]

    class Meta:
        model = Orders



