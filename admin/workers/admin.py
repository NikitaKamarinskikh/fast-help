from django.contrib import admin
from .models import Workers


@admin.register(Workers)
class WorkersAdmin(admin.ModelAdmin):
    list_display = ["name", "phone", "rating", "completed_orders_quantity"]
    search_fields = ["phone"]

    class Meta:
        model = Workers


