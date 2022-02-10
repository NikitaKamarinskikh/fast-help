from django.db import models
from admin.main.models import BotUsers, TimeBasedModel
from admin.main.models import JobCategories


class Workers(TimeBasedModel):
    user = models.ForeignKey(BotUsers, verbose_name="Пользователь", on_delete=models.CASCADE)
    name = models.CharField("Имя", max_length=255)
    location = models.CharField("Координаты", max_length=255)
    city = models.CharField("Город", default="Неизвестный", max_length=255)
    phone = models.CharField("Телефон", max_length=255)
    additional_contacts = models.CharField("Дополнительная информация", max_length=255, null=True, blank=True)
    rating = models.FloatField("Рейтинг", default=0.0)
    completed_orders_quantity = models.PositiveBigIntegerField("Количество выполненных заказов", default=0)

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


