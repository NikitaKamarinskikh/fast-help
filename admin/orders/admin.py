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
    inlines = [OrderCandidatesInline]

    class Meta:
        model = Orders



