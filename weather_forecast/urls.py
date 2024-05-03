from django.urls import path
from .views import services, openweathermap_forecast, accuweather_forecast, comparison

urlpatterns = [
    path('', services, name='Службы'),
    path('openweathermap/', openweathermap_forecast, name='OpenWeatherMap'),
    path('accuweather/', accuweather_forecast, name='AccuWeather'),
    path('comparison/', comparison, name='Сравнение'),
]
