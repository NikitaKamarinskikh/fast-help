# Generated by Django 3.1.14 on 2022-02-14 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_orders_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='status',
            field=models.CharField(default='Ожидает начала', max_length=120, verbose_name='Статус'),
        ),
    ]
