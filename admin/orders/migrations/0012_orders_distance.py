# Generated by Django 3.1.14 on 2022-03-09 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0011_auto_20220307_1857'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='distance',
            field=models.PositiveIntegerField(default=500, verbose_name='Дистанция'),
        ),
    ]
