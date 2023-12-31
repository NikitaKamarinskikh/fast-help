# Generated by Django 3.1.14 on 2022-02-27 12:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main', '0010_auto_20220227_0732'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transactions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата изменения')),
                ('amount', models.BigIntegerField(verbose_name='Сумма')),
                ('is_paid', models.BooleanField(default=False, verbose_name='Оплачена')),
                ('bot_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.botusers', verbose_name='Пользователь бота')),
            ],
            options={
                'verbose_name': 'Транзакция',
                'verbose_name_plural': 'Транзакции',
            },
        ),
    ]
