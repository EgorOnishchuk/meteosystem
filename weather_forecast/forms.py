from django.forms import Form, RegexField, ChoiceField
from django.urls import reverse
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from crispy_forms.bootstrap import TabHolder, Tab, StrictButton
from faker import Faker


class WeatherForecastForm(Form):
    locality = RegexField(
        r'^[А-Яа-я0-9]+(?:-[А-Яа-я0-9]+)*(?: [А-Яа-я0-9]+(?:-[А-Яа-я0-9]+)*)*$',
        max_length=168,
        label='',
        help_text='Введите название по-русски.',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.attrs = {
            'novalidate': '',
        }
        self.helper.form_class = 'needs-validation'


class AccuWeatherForm(WeatherForecastForm):
    CHOICES = (
        (0, 'Не указана'),
        (1, 'Завтра'),
        (2, 'Послезавтра'),
    )
    day = ChoiceField(choices=CHOICES,
                      label='',
                      help_text='Укажите дату прогноза или будет получена погода сейчас.')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.form_action = reverse('AccuWeather')
        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    'Сейчас',
                    css_id='now-accuweather',
                ),
                Tab(
                    'Прогноз',
                    Field(
                        'day',
                    ),
                    css_id='forecast-accuweather',
                ),
            ),
            Field(
                'locality',
                pattern='^[А-Яа-я0-9]+(?:-[А-Яа-я0-9]+)*(?: [А-Яа-я0-9]+(?:-[А-Яа-я0-9]+)*)*$',
                autocomplete='on',
                placeholder=Faker('ru_RU').city_name(),
            ),
            StrictButton(
                'Посмотреть прогноз погоды',
                css_class='btn-primary',
                type='submit',
            ),
        )


class OpenWeatherMapForm(WeatherForecastForm):
    CHOICES = (
        (0, 'Не указана'),
        (9, 'Завтра'),
        (17, 'Послезавтра'),
    )
    day = ChoiceField(choices=CHOICES,
                      label='',
                      help_text='Укажите дату прогноза или будет получена погода сейчас.'
                      )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.form_action = reverse('OpenWeatherMap')
        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    'Сейчас',
                    css_id='now-openweathermap'
                ),
                Tab(
                    'Прогноз',
                    Field(
                        'day',
                    ),
                    css_id='forecast-openweathermap',
                ),
            ),
            Field(
                'locality',
                pattern='^[А-Яа-я0-9]+(?:-[А-Яа-я0-9]+)*(?: [А-Яа-я0-9]+(?:-[А-Яа-я0-9]+)*)*$',
                autocomplete='on',
                placeholder=Faker('ru_RU').city_name(),
            ),
            StrictButton(
                'Посмотреть прогноз погоды',
                css_class='btn-primary',
                type='submit',
            ),
        )


class ComparisonForm(WeatherForecastForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.form_action = reverse('Сравнение')
        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    'Сейчас',
                    Field(
                        'locality',
                        pattern='^[А-Яа-я0-9]+(?:-[А-Яа-я0-9]+)*(?: [А-Яа-я0-9]+(?:-[А-Яа-я0-9]+)*)*$',
                        autocomplete='on',
                        placeholder=Faker('ru_RU').city_name(),
                    ),
                ),
            ),
            StrictButton(
                'Посмотреть прогноз погоды',
                css_class='btn-primary',
                type='submit',
            ),
        )
