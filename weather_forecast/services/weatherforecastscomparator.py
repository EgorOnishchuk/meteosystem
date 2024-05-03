from .weatherforecast import WeatherForecast


class WeatherForecastsComparator:
    """
    Сопоставление метеоданных от нескольких метеорологических служб.
    """
    Comparison = dict[str: list[str], str: str, str: dict[str: list[str]]] | dict[str: str]
    order = (
        'Погода',
        'Погода по ощущениям',
        'Погода по ощущениям в тени',
        'Минимальная текущая температура',
        'Максимальная текущая температура',
        'Атмосферное давление',
        'Скорость ветра',
        'Видимость',
        'Облачность',
        'Влажность на улице',
        'Влажность в помещении',
    )

    def __init__(self, *args: WeatherForecast) -> None:
        """
        Создаёт сопоставление.
        :param args: Метеорологические службы в виде объектов.
        """
        self.args = args

    def get_comparison(self, locality: str) -> Comparison:
        """
        Сравнивает текущую погоду.
        :param locality: Населённый пункт, для которого определяется погода.
        :return: Сравнение погоды, состоящие из названий метеорологических служб, населённого пункта и пар
                 "параметр погоды — данные по параметру". Если не удалось получить погоду от хотя бы одной
                 службы — только названия служб и населённого пункта.
        """
        forecasts = []
        for meteorological_service in self.args:
            forecast = meteorological_service.get_current_weather(locality)
            if not forecast.get('forecast'):
                return {
                    'locality': locality,
                    'forecasts': {},
                }
            forecasts.append(forecast)
        parameters = tuple(set.intersection(*[set(forecast['forecast'].keys()) for forecast in forecasts]))

        comparison = {
            'meteorological_services': [forecast['meteorological_service'] for forecast in forecasts],
            'locality': locality,
            'forecasts': {},
        }
        for parameter in parameters:
            comparison['forecasts'][parameter] = [forecast['forecast'][parameter] for forecast in forecasts]
        comparison['forecasts'] = dict(sorted(comparison['forecasts'].items(),
                                              key=lambda x: WeatherForecastsComparator.order.index(x[0])))

        return comparison
