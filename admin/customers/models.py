from django.db import models
from admin.main.models import BotUsers, TimeBasedModel


class Customers(TimeBasedModel):
    user = models.ForeignKey(BotUsers, verbose_name="Пользователь", on_delete=models.CASCADE)
    completed_orders_quantity = models.PositiveBigIntegerField("Количество завершенных заказов", default=0)
    rating = models.FloatField("Рейтинг", default=0.0)

    def __str__(self):
        return self.user.__str__()

    class Meta:
        verbose_name = "Заказчик"
        verbose_name_plural = "Заказчики"



