# Generated by Django 3.1.14 on 2022-02-13 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_botusers_referrer'),
    ]

    operations = [
        migrations.CreateModel(
            name='BotAdmins',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата изменения')),
                ('telegram_id', models.CharField(max_length=255, verbose_name='ID в телеграмме')),
                ('username', models.CharField(blank=True, max_length=255, null=True, verbose_name='Юзернейм в телеграмме')),
                ('name', models.CharField(max_length=255, verbose_name='Имя')),
            ],
            options={
                'verbose_name': 'Админ бота',
                'verbose_name_plural': 'Админы бота',
            },
        ),
    ]
