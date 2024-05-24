from .accuweather import AccuWeather
from .openweathermap import OpenWeatherMap
from .weatherforecastscomparator import WeatherForecastsComparator


class WeatherForecastManager:
    """
    Система управления прогнозом погоды. Обеспечивает единую точку входа для получения данных от
    метеорологической службы.
    """
    def __init__(self, meteorological_service: str, forecast_time: str, locality: str) -> None:
        """
        Создаёт систему управления прогнозом погоды.
        :param meteorological_service: Метеорологическая служба.
        :param forecast_time: Время прогноза погоды словом.
        :param locality: Населённый пункт, для которого определяется погода.
        """
        self.meteorological_service = meteorological_service
        self.forecast_time = forecast_time
        self.locality = locality

    def get_weather(self):
        """
        Запрашивает прогноз погоды по API метеорологической службы.
        :return: Прогноз погоды, состоящий из названий метеорологической службы, населённого пункта и пар
                 "параметр погоды — прогноз по параметру". Если прогноз получить не удалось — только названия
                 метеорологической службы и населённого пункта, а если для полученной метеорологической службы не
                 разработан алгоритм получения прогноза погоды — None.
        """
        _accuweather = AccuWeather(
            'AccuWeather',
            'City Search',
            '5 Days of Daily Forecasts',
            'Current Conditions'
        )

        _openweathermap = OpenWeatherMap(
            'OpenWeatherMap',
            'Geocoding',
            '5 Day / 3 Hour Forecast',
            'Current Weather Data',
        )

        _weather_forecast_comparator = WeatherForecastsComparator(
            _accuweather,
            _openweathermap,
        )

        _meteorological_services = {
            'AccuWeather': {
                'day_definition': {
                    'Сейчас': 0,
                    'Завтра': 1,
                    'Послезавтра': 2,
                },
                'forecasts': {
                    0: _accuweather.get_current_weather,
                    1: _accuweather.get_forecast,
                    2: _accuweather.get_forecast,
                },
            },
            'OpenWeatherMap': {
                'day_definition': {
                    'Сейчас': 0,
                    'Завтра': 9,
                    'Послезавтра': 17,
                },
                'forecasts': {
                    0: _openweathermap.get_current_weather,
                    9: _openweathermap.get_forecast,
                    17: _openweathermap.get_forecast,
                }
            },
            'Сравнение': {
                'day_definition': {
                    'Сейчас': 0,
                    'Завтра': 0,
                    'Послезавтра': 0,
                },
                'forecasts': {
                    0: _weather_forecast_comparator.get_current_weather
                },
            },
        }

        service = _meteorological_services.get(self.meteorological_service)
        if service is not None:
            day_definition = service['day_definition'][self.forecast_time]
            return service['forecasts'][day_definition](self.locality, day_definition) if day_definition \
                else service['forecasts'][day_definition](self.locality)
        return None
