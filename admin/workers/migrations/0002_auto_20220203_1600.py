# Generated by Django 3.1.14 on 2022-02-03 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workers', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='workercategories',
            options={'verbose_name': 'Категория исполнителя', 'verbose_name_plural': 'Категории исполнителей'},
        ),
        migrations.AddField(
            model_name='workers',
            name='additional_contacts',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Дополнительная информация'),
        ),
    ]