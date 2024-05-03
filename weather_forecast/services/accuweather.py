from requests import get
from datetime import datetime
from ..models import MeteorologicalAPI
from .weatherforecast import WeatherForecast


class AccuWeather(WeatherForecast):
    """
    Прогноз погоды от AccuWeather.
    """
    def __init__(self, meteorological_service: str, search_api: str, forecast_api: str, current_api: str) -> None:
        """
        Создаёт прогноз погоды от AccuWeather.
        :param meteorological_service: Название версии метеорологической службы, предоставляющей метеоданные.
        :param search_api: Название API, предоставляющего идентификатор населённого пункта по его названию.
        :param forecast_api: Название API, предоставляющего прогноз погоды.
        :param current_api: Название API, предоставляющего информацию о текущей погоде.
        """
        super().__init__(meteorological_service, forecast_api, current_api)
        self.search_api = search_api

    def _get_search_api(self) -> MeteorologicalAPI:
        """
        Запрашивает API, предоставляющий идентификатор населённого пункта по его названию, из базы данных.
        :return: API в виде объекта.
        """
        return self._get_meteorological_service().meteorologicalapi_set.get(name=self.search_api)

    def get_forecast(self, locality, day):
        """
        Запрашивает прогноз погоды по API.
        :param locality: Населённый пункт, для которого определяется прогноз погоды.
        :param day: Число, по которому определяется, на какой день предоставляется прогноз погоды: 1 — на завтра,
                    2 — на послезавтра.
        :return: Прогноз погоды, состоящий из названий метеорологической службы, населённого пункта и пар
                 "параметр погоды — прогноз по параметру". Если прогноз получить не удалось — только названия
                 метеорологической службы и населённого пункта.
        """
        search = self._get_search_api()

        parameters = {
            'apikey': search.key,
            'q': locality,
            'offset': 1,
        }
        response = get(search.url, parameters)
        if response.status_code != 200 or not response.json():
            return {
                'meteorological_service': self.meteorological_service,
                'locality': locality,
                'forecast': {},
            }
        key = response.json()[0]['Key']

        forecast = self._get_forecast_api()
        parameters = {
            'apikey': search.key,
            'language': 'ru-ru',
            'details': True,
            'metric': True,
        }
        response = get(f'{forecast.url}/{key}', parameters)
        if response.status_code != 200:
            return {
                'meteorological_service': self.meteorological_service,
                'locality': locality,
                'forecast': {},
            }
        response = response.json()
        main = response['DailyForecasts'][day]
        time = datetime.fromisoformat(main['Date']).astimezone().strftime('%d.%m.%Y')
        temperature = main['Temperature']
        feel_temperature = main['RealFeelTemperature']
        shade_temperature = main['RealFeelTemperatureShade']
        day_weather = main["Day"]
        night_weather = main["Night"]

        return {
            'meteorological_service': self.meteorological_service,
            'locality': f'{locality}, на {time}',
            'forecast': {
                'Ключевые события': response['Headline']['Text'],
                'Суточная температура': f'минимальная {round(temperature["Minimum"]["Value"])} ℃, '
                                        f'максимальная {round(temperature["Maximum"]["Value"])} ℃',
                'Суточная погода по ощущениям': f'минимальная {round(feel_temperature["Minimum"]["Value"])} ℃, '
                                                f'{feel_temperature["Minimum"]["Phrase"].lower()}. Максимальная '
                                                f'{round(feel_temperature["Maximum"]["Value"])} ℃,'
                                                f'{feel_temperature["Maximum"]["Phrase"].lower()}.',
                'Суточная погода по ощущениям в тени': f'минимальная {round(shade_temperature["Minimum"]["Value"])} ℃, '
                                                       f'{shade_temperature["Minimum"]["Phrase"].lower()}. '
                                                       f'Максимальная {round(shade_temperature["Maximum"]["Value"])} '
                                                       f'℃, {shade_temperature["Maximum"]["Phrase"].lower()}',
                'Погода днём': f'{day_weather["LongPhrase"]}',
                'Ветер днём': f'{round(day_weather["Wind"]["Speed"]["Value"] * 5 / 18)} м/c',
                'Влажность на улице днём': f'минимальная {round(day_weather["RelativeHumidity"]["Minimum"])} %, '
                                           f'максимальная {round(day_weather["RelativeHumidity"]["Maximum"])} %',
                'Погода ночью': f'{night_weather["LongPhrase"]}',
                'Ветер ночью': f'{round(night_weather["Wind"]["Speed"]["Value"] * 5 / 18)} м/с',
                'Влажность на улице ночью': f'минимальная {round(night_weather["RelativeHumidity"]["Minimum"])} %, '
                                            f'максимальная {round(night_weather["RelativeHumidity"]["Maximum"])} %',
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
        search = self._get_search_api()

        parameters = {
            'apikey': search.key,
            'q': locality,
            'offset': 1,
        }
        response = get(search.url, parameters)
        if response.status_code != 200 or not response.json():
            return {
                'meteorological_service': self.meteorological_service,
                'locality': locality,
                'forecast': {},
            }
        key = response.json()[0]['Key']

        forecast = self._get_current_api()
        parameters = {
            'apikey': search.key,
            'language': 'ru-ru',
            'details': True,
        }
        response = get(f'{forecast.url}/{key}', parameters)
        if response.status_code != 200:
            return {
                'meteorological_service': self.meteorological_service,
                'locality': locality,
                'forecast': {},
            }
        response = response.json()[0]
        feel_temperature = response["RealFeelTemperature"]["Metric"]
        shade_temperature = response["RealFeelTemperatureShade"]["Metric"]

        return {
            'meteorological_service': self.meteorological_service,
            'locality': locality,
            'forecast': {
                'Погода': f'{response["WeatherText"]}, {round(response["Temperature"]["Metric"]["Value"])} ℃',
                'Погода по ощущениям': f'{feel_temperature["Phrase"]}, {round(feel_temperature["Value"])} ℃',
                'Погода по ощущениям в тени': f'{shade_temperature["Phrase"]}, {round(shade_temperature["Value"])} ℃',
                'Атмосферное давление': f'{response["PressureTendency"]["LocalizedText"]}, '
                                        f'{round(response["Pressure"]["Metric"]["Value"] * 0.75)} мм рт. ст.',
                'Скорость ветра': f'{round(response["Wind"]["Speed"]["Metric"]["Value"] * 5 / 18)} м/с',
                'Видимость': f'{round(response["Visibility"]["Metric"]["Value"])} км',
                'Облачность': f'{round(response["CloudCover"])} %',
                'Влажность на улице': f'{round(response["RelativeHumidity"])} %',
                'Влажность в помещении': f'{round(response["IndoorRelativeHumidity"])} %',
            }
        }
