from django.db.models import (Model, CharField, TextField, PositiveSmallIntegerField, BooleanField, URLField,
                              ForeignKey, ManyToManyField, SET_NULL)


class MeteorologicalProvider(Model):
    class Meta:
        abstract = True

    name = CharField(
        'Название',
        unique=True,
        max_length=50,
    )

    def __str__(self):
        return self.name


class GeographicalCoverage(Model):
    class Meta:
        verbose_name = verbose_name_plural = 'Географическое покрытие'

    name = CharField(
        'Название',
        max_length=50,
    )

    def __str__(self):
        return self.name


class WeatherTime(Model):
    class Meta:
        verbose_name = verbose_name_plural = 'Время погоды'

    name = CharField(
        'Название',
        max_length=30,
    )

    def __str__(self):
        return self.name


class MeteorologicalParameter(Model):
    class Meta:
        verbose_name = 'Метеорологический параметр'
        verbose_name_plural = 'Метеорологические параметры'

    WEATHER_TIME_CHOICES = (
        ('Прогноз', 'Прогноз'),
        ('Сейчас', 'Сейчас'),
    )

    name = CharField(
        'Название',
        max_length=50,
    )
    unit = CharField(
        'Единица измерения',
        max_length=20,
    )
    weather_time = CharField(
        'Время погоды',
        max_length=20,
        choices=WEATHER_TIME_CHOICES,
    )
    importance = PositiveSmallIntegerField('Важность')

    def __str__(self):
        return f'{self.name}, {self.weather_time}'


class MeteorologicalService(MeteorologicalProvider):
    class Meta:
        verbose_name = 'Метеорологическая служба'
        verbose_name_plural = 'Метеорологические службы'

    description = TextField(
        'Описание',
        unique=True,
    )
    geographical_coverage = ForeignKey(
        GeographicalCoverage,
        on_delete=SET_NULL,
        null=True,
        verbose_name='Географическое покрытие',
    )
    foundation_year = PositiveSmallIntegerField('Год основания')
    official_url = URLField(
        'Официальный URL',
        unique=True,
    )
    weather_time = ManyToManyField(
        WeatherTime,
        verbose_name='Время погоды',
    )
    parameters = ManyToManyField(
        MeteorologicalParameter,
        verbose_name='Параметры',
    )
    
    is_active = BooleanField('Активен')


class MeteorologicalAPI(MeteorologicalProvider):
    class Meta:
        verbose_name = 'Метеорологический API'
        verbose_name_plural = 'Метеорологические API'

    url = URLField('URL')
    key = CharField(
        'Ключ',
        max_length=200,
    )
    meteorological_service = ForeignKey(
        MeteorologicalService,
        on_delete=SET_NULL,
        null=True,
        verbose_name='Метеорологическая служба'
    )
