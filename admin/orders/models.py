from django.db import models
from admin.main.models import TimeBasedModel, JobCategories
from admin.customers.models import Customers


class Orders(TimeBasedModel):
    customer = models.ForeignKey(Customers, verbose_name="Заказчик", on_delete=models.CASCADE)
    category = models.ForeignKey(JobCategories, verbose_name="Категория", on_delete=models.CASCADE)
    location = models.CharField("Локация", max_length=255)
    customer_phone = models.CharField("Телефон заказчика", max_length=255)
    customer_username = models.CharField("Юзернейм заказчика", max_length=30)
    additional_contacts = models.CharField("Дополнительные контакты", max_length=255)
    description = models.TextField("Описание")
    start_date = models.DateTimeField("Дата начала")
    execution_time = models.TimeField("Время выполнения")

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
