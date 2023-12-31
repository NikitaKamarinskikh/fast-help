from django.db import models
from admin.main.models import TimeBasedModel, JobCategories
from admin.customers.models import Customers
from admin.workers.models import Workers
from data.config import OrderStatuses


class Orders(TimeBasedModel):
    customer = models.ForeignKey(Customers, verbose_name="Заказчик", on_delete=models.CASCADE)
    customer_telegram_id = models.CharField("ID заказчика в телеграмме", default="", max_length=255)
    category = models.ForeignKey(JobCategories, verbose_name="Категория", on_delete=models.CASCADE)
    category_name = models.CharField("Название категории", max_length=255, null=True, blank=True)
    distance = models.PositiveIntegerField("Дистанция", default=500)
    worker = models.ForeignKey(Workers, verbose_name="Исполнитель", null=True, blank=True, on_delete=models.CASCADE)
    candidates = models.ManyToManyField(Workers, verbose_name="Кандидаты", related_name="order_candidates", blank=True,
                                        limit_choices_to={'telegram_id': 0})
    status = models.CharField("Статус", max_length=120, default=OrderStatuses.waiting_for_payment)
    customer_name = models.CharField("Имя для обращения к заказчику", max_length=255)
    location = models.CharField("Координаты", max_length=255)
    latitude = models.PositiveIntegerField("Целая часть от широты", default=0)
    longitude = models.PositiveIntegerField("Целая часть от долготы", default=0)
    city = models.CharField("Город", default="Неизвестный", max_length=255)
    customer_phone = models.CharField("Телефон заказчика", max_length=255)
    additional_contacts = models.CharField("Дополнительные контакты", max_length=255, null=True, blank=True)
    description = models.TextField("Описание", null=True, blank=True)
    voice_description = models.CharField("ID голосовухи с описанием задачи", max_length=255, null=True, blank=True)
    start_date = models.DateTimeField("Дата и время начала")
    execution_time = models.TimeField("Время выполнения")
    allow_to_write_in_telegram = models.BooleanField("Можно ли писать в телеграмм заказчику", default=False)

    def __str__(self):
        return f"{self.customer.__str__()} {self.category.name}"

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


class OrderCandidates(TimeBasedModel):
    worker = models.ForeignKey(Workers, verbose_name="Исполнитель", on_delete=models.CASCADE)
    order = models.ForeignKey(Orders, verbose_name="Заказ", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.worker.__str__()} {self.order.__str__()}"

    class Meta:
        verbose_name = "Кандидат"
        verbose_name_plural = "Кандидаты"


class OrdersTimestamps(models.Model):
    order = models.ForeignKey(Orders, verbose_name="Заказ", on_delete=models.CASCADE)
    seconds = models.PositiveBigIntegerField("Секунды")

    class Meta:
        verbose_name = "Временная отметка для заказа"
        verbose_name_plural = "Временные отметки для заказов"




