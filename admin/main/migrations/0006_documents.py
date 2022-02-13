# Generated by Django 3.1.14 on 2022-02-13 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_botadmins'),
    ]

    operations = [
        migrations.CreateModel(
            name='Documents',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата изменения')),
                ('name', models.CharField(max_length=255, verbose_name='Название документа')),
                ('telegram_id', models.CharField(max_length=255, verbose_name='ID документа в телеграмме')),
            ],
            options={
                'verbose_name': 'Документ',
                'verbose_name_plural': 'Документы',
            },
        ),
    ]
