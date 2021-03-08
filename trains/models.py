from django.db import models
from django.core.exceptions import ValidationError
from django.urls import reverse

from cities.models import City


class Train(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Train')
    travel_time = models.SmallIntegerField(verbose_name="Train's travel time")
    from_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='from_city_set',
                                  verbose_name='From city')
    # Строковое представление модели для недопущения ошибок, связанных с импортами
    # Так же, если есть связи в двух классах, и типо низя их использовать если класс написан ниже)), то можно вальнуть
    # строкой
    to_city = models.ForeignKey('cities.City', on_delete=models.CASCADE, related_name='to_city_set',
                                  verbose_name='To city')

    # def get_absolute_url(self):
    #     return reverse('trains:detail', kwargs={'pk': self.id})

    def __str__(self):
        return f'Train {self.name} from {self.from_city} to {self.to_city}.'

    class Meta:
        verbose_name = 'Train'
        verbose_name_plural = 'Trains'  # Отображение имени таблицы во множественном числе
        ordering = ['travel_time']  # Порядок отображения

    def clean(self):
        if self.from_city == self.to_city:
            raise ValidationError('The point of departure and arrival is the same')
        qs = Train.objects.filter(from_city=self.from_city, to_city=self.to_city,
                                  travel_time=self.travel_time).exclude(pk=self.id) # Исключения текущей записи
        # Train == self.__class__
        if qs.exists():
            raise ValidationError('Train with such conditions already exists')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)