# Generated by Django 3.1.14 on 2022-04-03 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workers', '0012_auto_20220317_1313'),
    ]

    operations = [
        migrations.AddField(
            model_name='workers',
            name='latitude',
            field=models.PositiveIntegerField(default=0, verbose_name='Целая часть от широты'),
        ),
        migrations.AddField(
            model_name='workers',
            name='longitude',
            field=models.PositiveIntegerField(default=0, verbose_name='Целая часть от долготы'),
        ),
    ]
