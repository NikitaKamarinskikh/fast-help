from django.contrib import admin
from .models import Workers, WorkerCategories


@admin.register(WorkerCategories)
class WorkerCategoriesAdmin(admin.ModelAdmin):

    class Meta:
        model = WorkerCategories


class WorkerCategoriesInline(admin.StackedInline):
    model = WorkerCategories
    extra = 0


@admin.register(Workers)
class WorkersAdmin(admin.ModelAdmin):
    inlines = [WorkerCategoriesInline]

    class Meta:
        model = Workers


