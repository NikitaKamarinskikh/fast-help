from django.db import models
from admin.main.models import BotUsers


class Customers(models.Model):
    user = models.ForeignKey(BotUsers, verbose_name="Пользователь", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Заказчик"
        verbose_name_plural = "Заказчики"



