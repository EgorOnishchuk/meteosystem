from django.contrib.admin import site, ModelAdmin
from .models import MeteorologicalService, MeteorologicalAPI, GeographicalCoverage, MeteorologicalParameter, WeatherTime


class MeteorologicalServiceAdmin(ModelAdmin):
    filter_horizontal = (
        'weather_time',
        'parameters',
    )


site.register(GeographicalCoverage)
site.register(MeteorologicalParameter)
site.register(MeteorologicalService, MeteorologicalServiceAdmin)
site.register(MeteorologicalAPI)
site.register(WeatherTime)
