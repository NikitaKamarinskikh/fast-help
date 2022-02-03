from django.db import models
from admin.main.models import BotUsers, TimeBasedModel


class Customers(TimeBasedModel):
    user = models.ForeignKey(BotUsers, verbose_name="Пользователь", on_delete=models.CASCADE)

    def __str__(self):
        return self.user.__str__()

    class Meta:
        verbose_name = "Заказчик"
        verbose_name_plural = "Заказчики"



