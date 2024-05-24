from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import meteorological_services, weather_forecast, weather_time

urlpatterns = [
    path('', meteorological_services, name='Метеорологические службы'),
    path('forecast/', weather_forecast, name='Прогноз погоды'),
    path('weathertime/', csrf_exempt(weather_time)),
]
