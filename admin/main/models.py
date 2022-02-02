from django.db import models


class TimeBasedModel(models.Model):
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата изменения', auto_now=True)

    class Meta:
        abstract = True


class Users(TimeBasedModel):
    telegram_id = models.CharField("ID в телеграмме", max_length=255)
    username = models.CharField("Юзернейм в телеграмме", max_length=255, blank=True, null=True)

    def __str__(self):
        if self.username:
            return self.username
        return self.telegram_id

    class Meta:
        abstract = True


class JobCategories(TimeBasedModel):
    name = models.CharField("Название категории", max_length=255)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

