from django.db import models
from django.contrib.auth import get_user_model


class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), related_name='profile', on_delete=models.CASCADE,
                                verbose_name='Пользователь')
    phone_number = models.CharField(max_length=20, null=False, blank=False, unique=True, verbose_name='номер телефона')
    address = models.CharField(max_length=60, null=True, blank=True, verbose_name='адрес')

    def __str__(self):
        return self.user.first_name + "'s Profile"

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"
