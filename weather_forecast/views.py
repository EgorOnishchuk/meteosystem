from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.db.models import Count
from json import loads
from .forms import WeatherForecastForm
from .models import MeteorologicalService, MeteorologicalParameter
from .services.weatherforecastmanager import WeatherForecastManager


@require_GET
def meteorological_services(request):
    return render(
        request,
        'weather_forecast/services.html',
        {
            'form': WeatherForecastForm(),
            'meteorological_services': [
                (
                    service,
                    [service.parameters.filter(weather_time=choice[0]).order_by('importance') for choice in
                     MeteorologicalParameter.WEATHER_TIME_CHOICES]
                )
                for service in MeteorologicalService.objects.all().annotate(cnt=Count('parameters')).order_by('-cnt')
            ],
        },
    )


@require_POST
def weather_forecast(request):
    form = WeatherForecastForm(request.POST)
    if form.is_valid():
        meteorological_service = form.cleaned_data['meteorological_service']
        forecast = WeatherForecastManager(
            meteorological_service,
            form.cleaned_data['forecast_time'],
            form.cleaned_data['locality'],
        ).get_weather()
        if forecast is None:
            return render(request, '400.html', status=400)
        elif meteorological_service != 'Сравнение':
            return render(
                request,
                'weather_forecast/single_forecast.html',
                {
                    'forecast': forecast,
                    'coverage': MeteorologicalService.objects.get(name=meteorological_service).geographical_coverage,
                },
            )
        else:
            return render(
                request,
                'weather_forecast/multiple_forecast.html',
                {
                    'forecast': forecast,
                    'coverage': MeteorologicalService.objects.get(name=meteorological_service).geographical_coverage,
                },
            )
    return render(request, '400.html', status=400)


@require_POST
def weather_time(request):
    return JsonResponse({'weather_time': [time.name for time in MeteorologicalService.objects.get(
        name=loads(request.body).get('meteorological_service')).weather_time.all()]})
