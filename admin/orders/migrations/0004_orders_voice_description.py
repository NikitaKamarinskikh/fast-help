# Generated by Django 3.1.14 on 2022-02-13 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_orders_worker'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='voice_description',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='ID голосовухи с описанием задачи'),
        ),
    ]
