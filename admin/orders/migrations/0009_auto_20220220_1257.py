# Generated by Django 3.1.14 on 2022-02-20 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workers', '0006_delete_workercategories'),
        ('orders', '0008_orders_candidates'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='candidates',
            field=models.ManyToManyField(blank=True, related_name='order_candidates', to='workers.Workers', verbose_name='Кандидаты'),
        ),
    ]
