from requests import get
from datetime import datetime
from ..models import MeteorologicalAPI
from .weatherforecast import WeatherForecast


class OpenWeatherMap(WeatherForecast):
    """
    Прогноз погоды от OpenWeatherMap.
    """
    def __init__(self, meteorological_service: str, geocoding_api: str, forecast_api: str, current_api: str,) -> None:
        """
        Создаёт прогноз погоды от OpenWeatherMap.
        :param meteorological_service: Название версии метеорологической службы, предоставляющей метеоданные.
        :param geocoding_api: Название API, предоставляющего координаты населённого пункта по его названию.
        :param forecast_api: Название API, предоставляющего прогноз погоды.
        :param current_api: Название API, предоставляющего информацию о текущей погоде.
        """
        super().__init__(meteorological_service, forecast_api, current_api)
        self.geocoding_api = geocoding_api

    def _get_geocoding_api(self) -> MeteorologicalAPI:
        """
        Запрашивает API, предоставляющий координаты населённого пункта по его названию.
        :return: API в виде объекта.
        """
        return self._get_meteorological_service().meteorologicalapi_set.get(name=self.geocoding_api)

    def get_forecast(self, locality, day):
        """
        Запрашивает прогноз погоды по API.
        :param locality: Населённый пункт, для которого определяется прогноз погоды.
        :param day: Число, по которому определяется, на какой день предоставляется прогноз погоды: 9 — на завтра,
        17 — на послезавтра.
        :return: Прогноз погоды, состоящий из названий метеорологической службы, населённого пункта и пар
                 "параметр погоды — прогноз по параметру". Если прогноз получить не удалось — только названия
                 метеорологической службы и населённого пункта.
        """
        geocoding = self._get_geocoding_api()

        parameters = {
            'q': locality,
            'limit': '1',
            'appid': geocoding.key,
        }
        response = get(geocoding.url, parameters)
        if response.status_code != 200 or not response.json():
            return {
                'meteorological_service': self.meteorological_service,
                'locality': locality,
                'forecast': {},
            }
        response = response.json()[0]

        forecast = self._get_forecast_api()
        parameters = {
            'lat': response['lat'],
            'lon': response['lon'],
            'appid': forecast.key,
            'cnt': day,
            'units': 'metric',
            'lang': 'ru',
        }
        response = get(forecast.url, parameters)
        if response.status_code != 200:
            return {
                'meteorological_service': self.meteorological_service,
                'locality': locality,
                'forecast': {},
            }
        response = response.json()['list'][day - 1]
        time = (datetime.strptime(response["dt_txt"], "%Y-%m-%d %H:%M:%S").astimezone()
                .strftime('%d.%m.%Y %H:%M'))
        main = response['main']

        return {
            'meteorological_service': self.meteorological_service,
            'locality': locality,
            'time': time,
            'forecast': {
                'Погода': f'{response["weather"][0]["description"]}, {round(main["temp"])} ℃',
                'Погода по ощущениям': f'{round(main["temp"])} ℃',
                'Атмосферное давление': f'{round(main["pressure"] * 0.75)} мм рт. ст.',
                'Минимальная текущая температура': f'{round(main["temp_min"])} ℃',
                'Максимальная текущая температура': f'{round(main["temp_max"])} ℃',
                'Скорость ветра': f'{round(response["wind"]["speed"])} м/с',
                'Облачность': f'{round(response["clouds"]["all"])} %',
                'Влажность на улице': f'{round(main["humidity"])} %',
            }
        }

    def get_current_weather(self, locality):
        """
        Запрашивает прогноз погоды по API.
        :param locality: Населённый пункт, для которого определяется прогноз погоды.
        :return: Прогноз погоды, состоящий из названий метеорологической службы, населённого пункта и пар
                 "параметр погоды — прогноз по параметру". Если прогноз получить не удалось — только названия
                 метеорологической службы и населённого пункта.
        """
        geocoding = self._get_geocoding_api()

        parameters = {
            'q': locality,
            'limit': '1',
            'appid': geocoding.key,
        }
        response = get(geocoding.url, parameters)
        if response.status_code != 200 or not response.json():
            return {
                'meteorological_service': self.meteorological_service,
                'locality': locality,
                'forecast': {},
            }
        response = response.json()[0]

        forecast = self._get_current_api()
        parameters = {
            'lat': response['lat'],
            'lon': response['lon'],
            'appid': forecast.key,
            'units': 'metric',
            'lang': 'ru',
        }
        response = get(forecast.url, parameters)
        if response.status_code != 200:
            return {
                'meteorological_service': self.meteorological_service,
                'locality': locality,
                'forecast': {},
            }
        response = response.json()
        main = response['main']

        return {
            'meteorological_service': self.meteorological_service,
            'locality': locality,
            'forecast': {
                'Погода': f'{response["weather"][0]["description"]}, {round(main["temp"])} ℃',
                'Погода по ощущениям': f'{round(main["feels_like"])} ℃',
                'Атмосферное давление': f'{round(main["pressure"] * 0.75)} мм рт. ст.',
                'Минимальная текущая температура': f'{round(main["temp_min"])} ℃',
                'Максимальная текущая температура': f'{round(main["temp_max"])} ℃',
                'Скорость ветра': f'{round(response["wind"]["speed"])} м/с',
                'Облачность': f'{round(response["clouds"]["all"])} %',
                'Влажность на улице': f'{round(main["humidity"])} %',
            },
        }
