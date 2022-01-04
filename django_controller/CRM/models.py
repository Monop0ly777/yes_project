from django.db import models


# Create your models here.
# Create your models here.
class TimeBaseModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)


class Purchase(TimeBaseModel):
    class Meta:
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'
        db_table = 'purchase'

    CHOICES = (
        ('Новый', 'Новый'),
        ('Обрабатывается', 'Обрабатывается'),
        ('Выполнен', 'Выполнен'),
    )
    name = models.CharField(verbose_name='Название товара', max_length=100)
    status = models.CharField(verbose_name='Статус заказа', max_length=50, choices=CHOICES)
    quantity = models.IntegerField(verbose_name='Количество')
    sum = models.IntegerField(verbose_name='Сумма заказа')
    number = models.CharField(verbose_name='Номер телефона', max_length=20)
    login = models.CharField(verbose_name='Логин в телеграме', max_length=100)
    user_id = models.BigIntegerField(unique=False, verbose_name='Уникальный ID telegram')

    def __str__(self):
        return f"{self.name} - {self.sum}"


class Purchase_Confirmed(TimeBaseModel):
    class Meta:
        verbose_name = 'Покупка Выполненная'
        verbose_name_plural = 'Покупки Выполненные'
        db_table = 'purchase_confirmed'

    CHOICES = (
        ('Новый', 'Новый'),
        ('Обрабатывается', 'Обрабатывается'),
        ('Выполнен', 'Выполнен'),
    )
    name = models.CharField(verbose_name='Название товара', max_length=100)
    status = models.CharField(verbose_name='Статус заказа', max_length=50, choices=CHOICES)
    quantity = models.IntegerField(verbose_name='Количество')
    sum = models.IntegerField(verbose_name='Сумма заказа')
    number = models.CharField(verbose_name='Номер телефона', max_length=20)
    login = models.CharField(verbose_name='Логин в телеграме', max_length=100)
    user_id = models.BigIntegerField(unique=False, verbose_name='Уникальный ID telegram')

    def __str__(self):
        return f"{self.name} - {self.sum}"

class Promocodes_orders(TimeBaseModel):
    class Meta:
        verbose_name = 'Покупка промокод'
        verbose_name_plural = 'Покупки промокодов'
        db_table = 'promocodes_orders'


    name = models.CharField(verbose_name='Название товара', max_length=100)
    quantity = models.IntegerField(verbose_name='Количество')
    sum = models.IntegerField(verbose_name='Сумма заказа')
    login = models.CharField(verbose_name='Логин в телеграме', max_length=100)
    user_id = models.BigIntegerField(unique=False, verbose_name='Уникальный ID telegram')
    data = models.CharField(verbose_name='Промокод', max_length=200, null=True)
    def __str__(self):
        return f"{self.name} - {self.sum}"