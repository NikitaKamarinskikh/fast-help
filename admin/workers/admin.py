from django.contrib import admin
from .models import Workers


@admin.register(Workers)
class WorkersAdmin(admin.ModelAdmin):

    class Meta:
        model = Workers


