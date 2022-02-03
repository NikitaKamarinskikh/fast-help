from django.db import models
from admin.main.models import BotUsers, TimeBasedModel
from admin.main.models import JobCategories


class Workers(TimeBasedModel):
    # categories
    user = models.ForeignKey(BotUsers, verbose_name="Пользователь", on_delete=models.CASCADE)
    name = models.CharField("Имя", max_length=255)
    location = models.CharField("Локация", max_length=255)
    phone = models.CharField("Телефон", max_length=255)

    def __str__(self):
        return self.user.__str__()

    class Meta:
        verbose_name = "Исполнитель"
        verbose_name_plural = "Исполнители"


class WorkerCategories(TimeBasedModel):
    worker = models.ForeignKey(Workers, verbose_name="Работник", on_delete=models.CASCADE)
    category = models.ForeignKey(JobCategories, verbose_name="Категория", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Категория исполнителя"
        verbose_name_plural = "Категории исполнителей"


