from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Profile(models.Model):
    name = models.CharField(max_length=160, verbose_name='Имя')
    phone = PhoneNumberField(verbose_name='Телефон')

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return self.name


class Barcode(models.Model):
    type = models.CharField(max_length=10)
    data = models.CharField(max_length=60)
    quality = models.CharField(max_length=10)
    image = models.ImageField(blank=True)

    def __str__(self):
        return f'type: {self.type}, data: {self.data}, quality: {self.quality}'
