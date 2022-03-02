# Generated by Django 3.1.14 on 2022-03-02 04:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workers', '0007_workers_is_privacy_policy_confirmed'),
    ]

    operations = [
        migrations.AddField(
            model_name='workers',
            name='orders_at_longer_distance_access_time',
            field=models.PositiveBigIntegerField(default=0, verbose_name='Срок окончания доступа к заданиям на больщей дистанции'),
        ),
    ]
