# Generated by Django 3.2.9 on 2021-12-27 22:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CRM', '0006_delete_promocodes_orders'),
    ]

    operations = [
        migrations.CreateModel(
            name='Promocodes_orders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100, verbose_name='Название товара')),
                ('quantity', models.IntegerField(verbose_name='Количество')),
                ('sum', models.IntegerField(verbose_name='Сумма заказа')),
                ('login', models.CharField(max_length=100, verbose_name='Логин в телеграме')),
                ('user_id', models.BigIntegerField(verbose_name='Уникальный ID telegram')),
                ('data', models.CharField(max_length=200, null=True, verbose_name='Промокод')),
            ],
            options={
                'verbose_name': 'Покупка промокод',
                'verbose_name_plural': 'Покупки промокодов',
                'db_table': 'promocodes_orders',
            },
        ),
    ]