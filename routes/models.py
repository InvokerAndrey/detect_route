from django.db import models

from cities.models import City


class Route(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Route')
    total_travel_time = models.SmallIntegerField(verbose_name="Total travel time")
    from_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='route_from_city_set',
                                  verbose_name='From city')
    # Строковое представление модели для недопущения ошибок, связанных с импортами
    # Так же, если есть связи в двух классах, и типо низя их использовать если класс написан ниже)), то можно вальнуть
    # строкой
    to_city = models.ForeignKey('cities.City', on_delete=models.CASCADE, related_name='route_to_city_set',
                                  verbose_name='To city')
    trains = models.ManyToManyField('trains.Train', verbose_name='Trains list')

    # def get_absolute_url(self):
    #     return reverse('trains:detail', kwargs={'pk': self.id})

    def __str__(self):
        return f'Route {self.name} from {self.from_city} to {self.to_city}.'

    class Meta:
        verbose_name = 'Route'
        verbose_name_plural = 'Routes'  # Отображение имени таблицы во множественном числе
        ordering = ['total_travel_time']  # Порядок отображения
