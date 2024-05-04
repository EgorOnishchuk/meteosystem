from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST
from .models import MeteorologicalService
from .forms import OpenWeatherMapForm, AccuWeatherForm, ComparisonForm
from .services.openweathermap import OpenWeatherMap
from .services.accuweather import AccuWeather
from .services.weatherforecastscomparator import WeatherForecastsComparator


@require_GET
def services(request):
    return render(
        request,
        'weather_forecast/services.html',
        {
            'meteorological_services': [
                (MeteorologicalService.objects.get(name='AccuWeather'), AccuWeatherForm()),
                (MeteorologicalService.objects.get(name='OpenWeatherMap'), OpenWeatherMapForm()),
                (MeteorologicalService.objects.get(name='Сравнение'), ComparisonForm()),
            ]
        }
    )


@require_POST
def accuweather_forecast(request):
    form = AccuWeatherForm(request.POST)

    if form.is_valid():
        locality = form.cleaned_data['locality']
        day = int(form.cleaned_data['day'])
        accuweather = AccuWeather('AccuWeather',
                                  'City Search',
                                  '5 Days of Daily Forecasts',
                                  'Current Conditions')

        if day == 0:
            return render(
                request,
                'weather_forecast/single_forecast.html',
                accuweather.get_current_weather(locality)
            )
        return render(
            request,
            'weather_forecast/single_forecast.html',
            accuweather.get_forecast(locality, day),
        )

    return render(request, '400.html', status=400)


@require_POST
def openweathermap_forecast(request):
    form = OpenWeatherMapForm(request.POST)

    if form.is_valid():
        locality = form.cleaned_data['locality']
        day = int(form.cleaned_data['day'])
        openweathermap = OpenWeatherMap('OpenWeatherMap',
                                        'Geocoding',
                                        '5 Day / 3 Hour Forecast',
                                        'Current Weather Data',
                                        )

        if day == 0:
            return render(
                request,
                'weather_forecast/single_forecast.html',
                openweathermap.get_current_weather(locality),
            )
        return render(
            request,
            'weather_forecast/single_forecast.html',
            openweathermap.get_forecast(locality, day),
        )

    return render(request, '400.html', status=400)


@require_POST
def comparison(request):
    form = ComparisonForm(request.POST)

    if form.is_valid():
        return render(
            request,
            'weather_forecast/multiple_forecast.html',
            WeatherForecastsComparator(AccuWeather('AccuWeather',
                                                   'City Search',
                                                   '5 Days of Daily Forecasts',
                                                   'Current Conditions'),
                                       OpenWeatherMap('OpenWeatherMap',
                                                      'Geocoding',
                                                      '5 Day / 3 Hour Forecast',
                                                      'Current Weather Data'),
                                       ).get_comparison(form.cleaned_data['locality'])
        )

    return render(request, '400.html', status=400)
