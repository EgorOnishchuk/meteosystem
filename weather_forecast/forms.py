from django.forms import Form, RegexField, ChoiceField
from django.utils.safestring import mark_safe
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from crispy_forms.bootstrap import PrependedText, StrictButton
from .models import MeteorologicalService, WeatherTime
from faker import Faker


class WeatherForecastForm(Form):
    meteorological_service = ChoiceField(
        choices=((meteorological_service, meteorological_service) for meteorological_service in
                 MeteorologicalService.objects.all()),
        label='',
        help_text='Выберите поставщика метеоданных.',
    )

    forecast_time = ChoiceField(
        choices=((weather_time, weather_time) for weather_time in WeatherTime.objects.all()),
        label='',
        help_text='Выберите время погоды.',
    )

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
        self.helper.form_action = 'forecast/'
        self.helper.attrs = {
            'novalidate': '',
        }
        self.helper.form_class = 'needs-validation'
        self.helper.layout = Layout(
            PrependedText(
                'meteorological_service',
                mark_safe('<i class="bi bi-building"></i>'),
            ),
            PrependedText(
                'forecast_time',
                mark_safe('<i class="bi bi-calendar3"></i>'),
            ),
            PrependedText(
                'locality',
                mark_safe('<i class="bi bi-geo-alt"></i>'),
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
