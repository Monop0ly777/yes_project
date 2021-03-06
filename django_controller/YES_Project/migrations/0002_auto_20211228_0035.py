# Generated by Django 3.2.9 on 2021-12-27 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('YES_Project', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Promocodes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('index', models.CharField(max_length=100, verbose_name='Индекс промокода')),
                ('data', models.CharField(max_length=200, verbose_name='Данные промокода')),
            ],
            options={
                'verbose_name': 'Промокод',
                'verbose_name_plural': 'Промокоды',
                'db_table': 'promocodes',
            },
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100, verbose_name='Имя пользователя')),
                ('user_id', models.BigIntegerField(unique=True, verbose_name='Уникальный ID telegram')),
                ('position', models.CharField(choices=[('Админ', 'Админ'), ('Менеджер', 'Менеджер')], max_length=50, verbose_name='Должность')),
            ],
            options={
                'verbose_name': 'Сотрудник',
                'verbose_name_plural': 'Сотрудники',
                'db_table': 'staff',
            },
        ),
        migrations.AlterField(
            model_name='items',
            name='created_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='items',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='items',
            name='promocode_index',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Ключ промокода'),
        ),
        migrations.AlterField(
            model_name='items',
            name='text',
            field=models.TextField(max_length=200, verbose_name='Описание товара'),
        ),
        migrations.AlterField(
            model_name='items',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='created_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
