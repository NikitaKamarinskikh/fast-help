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
    categories = models.ManyToManyField(JobCategories, verbose_name="Категории")
    is_privacy_policy_confirmed = models.BooleanField("Подтверждена ли политика конфиденциальности", default=False)
    orders_at_longer_distance_access_time = models.PositiveBigIntegerField(
        "Срок окончания доступа к заданиям на больщей дистанции", default=0)
    max_distance = models.IntegerField("Максимальная дистанция для заказов в метрах", default=500)

    def __str__(self):
        return self.user.__str__()

    class Meta:
        verbose_name = "Исполнитель"
        verbose_name_plural = "Исполнители"


