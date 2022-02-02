from django.contrib import admin
from . import models


@admin.register(models.JobCategories)
class JobCategoriesAdmin(admin.ModelAdmin):
    list_display = ["name"]

    class Meta:
        model = models.JobCategories
