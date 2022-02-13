from django.contrib import admin
from . import models


@admin.register(models.JobCategories)
class JobCategoriesAdmin(admin.ModelAdmin):
    list_display = ["name"]

    class Meta:
        model = models.JobCategories


@admin.register(models.BotUsers)
class BotUsersAdmin(admin.ModelAdmin):

    class Meta:
        model = models.BotUsers


@admin.register(models.BotAdmins)
class BotAdminsAdmin(admin.ModelAdmin):

    class Meta:
        model = models.BotAdmins


@admin.register(models.Documents)
class DocumentsAdmin(admin.ModelAdmin):

    class Meta:
        model = models.Documents

