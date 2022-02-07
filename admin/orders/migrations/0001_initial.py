# Generated by Django 3.1.14 on 2022-02-07 08:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main', '0002_botusers'),
        ('customers', '0003_auto_20220203_0847'),
    ]

    operations = [
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата изменения')),
                ('customer_name', models.CharField(max_length=255, verbose_name='Имя для обращения к заказчику')),
                ('location', models.CharField(max_length=255, verbose_name='Координаты')),
                ('city', models.CharField(default='Неизвестный', max_length=255, verbose_name='Город')),
                ('customer_phone', models.CharField(max_length=255, verbose_name='Телефон заказчика')),
                ('additional_contacts', models.CharField(blank=True, max_length=255, null=True, verbose_name='Дополнительные контакты')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('start_date', models.DateTimeField(verbose_name='Дата и время начала')),
                ('execution_time', models.TimeField(verbose_name='Время выполнения')),
                ('allow_to_write_in_telegram', models.BooleanField(default=False, verbose_name='Можно ли писать в телеграмм заказчику')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.jobcategories', verbose_name='Категория')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customers.customers', verbose_name='Заказчик')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
            },
        ),
    ]
