from django.db import models
from django import forms


# Create your models here.
class TimeBaseModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)


class Users(TimeBaseModel):
    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        db_table = 'users'

    id = models.AutoField(primary_key=True)
    user_id = models.BigIntegerField(unique=True, verbose_name='Уникальный ID telegram')
    name = models.CharField(verbose_name='Имя пользователя', max_length=50)
    yes_coin_balance = models.IntegerField(verbose_name='Баланс YesCoin', default=0)

    def __str__(self):
        return f"{self.name} - {self.yes_coin_balance}"


class Items(TimeBaseModel):
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        db_table = 'items'

    name = models.CharField(verbose_name='Название товара', max_length=50)
    price = models.IntegerField(verbose_name='Цена')
    text = models.TextField(max_length=200, verbose_name='Описание товара')

    category_name = models.CharField(verbose_name='Название категории', max_length=50)
    category_code = models.CharField(verbose_name='Код категории', max_length=20)
    subcategory_name = models.CharField(verbose_name='Название подкатегории', max_length=50)
    subcategory_code = models.CharField(verbose_name='Код подкатегории', max_length=50)

    promocode_index = models.CharField(max_length=20, verbose_name='Ключ промокода', blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.price}"


class Staff(TimeBaseModel):
    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'
        db_table = 'staff'

    CHOICES = (
        ('Админ', 'Админ'),
        ('Менеджер', 'Менеджер'),
    )
    name = models.CharField(verbose_name='Имя пользователя', max_length=100)
    user_id = models.BigIntegerField(unique=True, verbose_name='Уникальный ID telegram')
    position = models.CharField(verbose_name='Должность', max_length=50, choices=CHOICES)

    def __str__(self):
        return f"{self.user_id} - {self.position}"


class Promocodes(TimeBaseModel):
    class Meta:
        verbose_name = 'Промокод'
        verbose_name_plural = 'Промокоды'
        db_table = 'promocodes'

    index = models.CharField(verbose_name='Индекс промокода', max_length=100)
    data = models.CharField(verbose_name='Данные промокода', max_length=200)

    def __str__(self):
        return f"{self.index} - {self.data}"


