from django.db import models


class TimeBasedModel(models.Model):
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата изменения', auto_now=True)

    class Meta:
        abstract = True


class BaseUser(TimeBasedModel):
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

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class BotUsers(BaseUser):
    referrer = models.ForeignKey("BotUsers", verbose_name="Приведен пользователем", on_delete=models.SET_NULL,
                                 blank=True, null=True)
    coins = models.BigIntegerField("Количество монет", default=0)


    class Meta:
        verbose_name = "Пользователь бота"
        verbose_name_plural = "Пользователи бота"


class BotAdmins(BaseUser):
    name = models.CharField("Имя", max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Админ бота"
        verbose_name_plural = "Админы бота"


class Documents(TimeBasedModel):
    choices = [
        ("customers", "Заказчики"),
        ("workers", "Исполнители"),
    ]
    users_category = models.CharField("Категория пользователей", max_length=255, choices=choices)
    name = models.CharField("Название документа", max_length=255)
    telegram_id = models.CharField("ID документа в телеграмме", max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Документ"
        verbose_name_plural = "Документы"





