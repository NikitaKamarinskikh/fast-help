from django.contrib import admin
from .models import Customers


@admin.register(Customers)
class CustomersAdmin(admin.ModelAdmin):
    list_display = ["user", "rating", "completed_orders_quantity"]

    class Meta:
        model = Customers


