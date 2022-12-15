from django.db import models
from django.urls import reverse

import ebay.models

CATEGORY_CHOICES = [('food', 'еда'), ('toys', 'игрушки'), ('stationary', 'канцелярия'), ('books', 'книги'), ('other', 'другое')]

#
# class Category(models.Model):
#     name = models.CharField(max_length=50, null=False, blank=False, verbose_name='название')


class Product(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, verbose_name='наименование')
    description = models.TextField(max_length=2000, null=True, blank=True, verbose_name='описание')
    category = models.CharField(
        max_length=100,
        null=False, blank=False,
        choices=CATEGORY_CHOICES,
        default=CATEGORY_CHOICES[4][0],
        verbose_name='категория')
    remainder = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return f'{self.name}_(id: {self.id})'

    def get_absolute_url(self):
        return reverse('view_product', kwargs={'pk': self.pk})

    def get_total_number(self):
        total = Product.objects.all().count()
        return total


class Basket(models.Model):
    product = models.ForeignKey('ebay.Product', related_name='basket', on_delete=models.DO_NOTHING,
                                verbose_name='продукт', null=True, blank=True)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.product.name} - {self.quantity}'

    def get_product_total(self):
        return self.quantity * self.product.price


class OrderProduct(models.Model):
    product = models.ForeignKey('ebay.Product', related_name='product_order', on_delete=models.DO_NOTHING,
                                verbose_name='продукт')
    order = models.ForeignKey('ebay.Order', related_name='order_product', on_delete=models.DO_NOTHING,
                              verbose_name='заказы')
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.product} | {self.order}'


class Order(models.Model):
    product = models.ManyToManyField('ebay.Product', related_name='orders', through='ebay.OrderProduct',
                                     through_fields=('order', 'product'), blank=True)
    user_name = models.CharField(max_length=50, null=False, blank=False, verbose_name='имя')
    phone = models.CharField(max_length=60, null=False, blank=False, verbose_name='номер телефона')
    address = models.CharField(max_length=100, null=False, blank=False, verbose_name='адрес')
    created_at = models.DateTimeField(auto_now_add=True)
