from django.db import models
from admin.main.models import TimeBasedModel, JobCategories
from admin.customers.models import Customers


class Orders(TimeBasedModel):
    customer = models.ForeignKey(Customers, verbose_name="Заказчик", on_delete=models.CASCADE)
    category = models.ForeignKey(JobCategories, verbose_name="Категория", on_delete=models.CASCADE)
    customer_name = models.CharField("Имя для обращения к заказчику", max_length=255)
    location = models.CharField("Координаты", max_length=255)
    city = models.CharField("Город", default="Неизвестный", max_length=255)
    customer_phone = models.CharField("Телефон заказчика", max_length=255)
    additional_contacts = models.CharField("Дополнительные контакты", max_length=255, null=True, blank=True)
    description = models.TextField("Описание", null=True, blank=True)
    start_date = models.DateTimeField("Дата и время начала")
    execution_time = models.TimeField("Время выполнения")
    allow_to_write_in_telegram = models.BooleanField("Можно ли писать в телеграмм заказчику", default=False)

    def __str__(self):
        return f"{self.customer.__str__()} {self.category.name}"

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"



