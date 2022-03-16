from django.db import models
from admin.main.models import TimeBasedModel, BotUsers


class Transactions(TimeBasedModel):
    bot_user = models.ForeignKey(BotUsers, verbose_name="Пользователь бота", on_delete=models.CASCADE)
    amount = models.BigIntegerField("Сумма")
    is_paid = models.BooleanField("Оплачена", default=False)

    class Meta:
        verbose_name = "Транзакция"
        verbose_name_plural = "Транзакции"


class Withdrawals(TimeBasedModel):
    user = models.ForeignKey(BotUsers, verbose_name="Пользователь бота", on_delete=models.CASCADE)
    coins_before = models.PositiveBigIntegerField("Монеты до")
    coins = models.PositiveBigIntegerField("Монеты")
    coins_after = models.PositiveBigIntegerField("Монетыпосле")

    class Meta:
        verbose_name = "Вывод средств"
        verbose_name_plural = "Выводы средств"


