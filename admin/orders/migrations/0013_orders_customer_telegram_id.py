# Generated by Django 3.1.14 on 2022-03-09 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0012_orders_distance'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='customer_telegram_id',
            field=models.PositiveIntegerField(default=0, verbose_name='ID заказчика в телеграмме'),
        ),
    ]
