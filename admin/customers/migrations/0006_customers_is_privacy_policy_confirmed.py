# Generated by Django 3.1.14 on 2022-02-21 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0005_customers_completed_orders_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='customers',
            name='is_privacy_policy_confirmed',
            field=models.BooleanField(default=False, verbose_name='Подтверждена ли политика конфиденциальности'),
        ),
    ]