from django.db import models
from django.urls import reverse


class City(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='City')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'City'
        verbose_name_plural = 'Cities'      # Отображение имени таблицы во множественном числе
        ordering = ['name']                 # Порядок отображения

    def get_absolute_url(self):
        return reverse('cities:detail', kwargs={'pk': self.id})