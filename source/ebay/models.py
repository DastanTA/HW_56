from django.db import models
from django.urls import reverse

CATEGORY_CHOICES = [('food', 'еда'), ('toys', 'игрушки'), ('stationary', 'канцелярия'), ('books', 'книги'), ('other', 'другое')]


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
