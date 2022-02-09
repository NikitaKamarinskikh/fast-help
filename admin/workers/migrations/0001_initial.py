# Generated by Django 3.1.14 on 2022-02-03 08:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main', '0002_botusers'),
    ]

    operations = [
        migrations.CreateModel(
            name='Workers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата изменения')),
                ('name', models.CharField(max_length=255, verbose_name='Имя')),
                ('location', models.CharField(max_length=255, verbose_name='Локация')),
                ('phone', models.CharField(max_length=255, verbose_name='Телефон')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.botusers', verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Исполнитель',
                'verbose_name_plural': 'Исполнители',
            },
        ),
        migrations.CreateModel(
            name='WorkerCategories',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата изменения')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.jobcategories', verbose_name='Категория')),
                ('worker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workers.workers', verbose_name='Работник')),
            ],
            options={
                'verbose_name': 'Категория исполнителя',
                'verbose_name_plural': 'Категории пользователей',
            },
        ),
    ]