# Generated by Django 3.1.14 on 2022-02-15 02:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_documents_users_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documents',
            name='users_category',
            field=models.CharField(choices=[('customers', 'Заказчики'), ('workers', 'Исполнители')], max_length=255, verbose_name='Категория пользователей'),
        ),
    ]
