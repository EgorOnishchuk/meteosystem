from abc import ABC, abstractmethod
from ..models import MeteorologicalService, MeteorologicalAPI


class WeatherForecast(ABC):
    """
    Прогноз погоды по стороннему интерфейсу программирования приложения.
    """
    Forecast = dict[str: str, str: str, dict[str: str]] | dict[str: str, str: str, dict: None]

    def __init__(self, meteorological_service: str, forecast_api: str, current_api: str) -> None:
        """
        Создаёт прогноз погоды. Промежуточные API, например для определения населённого пункта по координатам,
        добавляются параметрами при переопределении метода.
        :param meteorological_service: Название версии метеорологической службы, предоставляющей метеоданные.
        :param forecast_api: Название API, предоставляющего прогноз погоды.
        :param current_api: Название API, предоставляющего информацию о текущей погоде.
        """
        self.meteorological_service = meteorological_service
        self.forecast_api = forecast_api
        self.current_api = current_api

    def _get_meteorological_service(self) -> MeteorologicalService:
        """
        Запрашивает метеорологическую службу из базы данных.
        :return: Метеорологическая служба в виде объекта.
        """
        return MeteorologicalService.objects.get(name=self.meteorological_service)

    def _get_forecast_api(self) -> MeteorologicalAPI:
        """
        Запрашивает API, предоставляющий непосредственно прогноз погоды, из базы данных.
        :return: API в виде объекта.
        """
        return self._get_meteorological_service().meteorologicalapi_set.get(name=self.forecast_api)

    def _get_current_api(self) -> MeteorologicalAPI:
        """
        Запрашивает API, предоставляющий непосредственно текущую погоду, из базы данных.
        :return: API в виде объекта.
        """
        return self._get_meteorological_service().meteorologicalapi_set.get(name=self.current_api)

    @abstractmethod
    def get_forecast(self, locality: str, day: int) -> Forecast:
        """
        Запрашивает прогноз погоды по API.
        :param locality: Населённый пункт, для которого определяется прогноз погоды.
        :param day: Число, по которому определяется, на какой день предоставляется прогноз погоды.
        :return: Прогноз погоды, состоящий из названий метеорологической службы, населённого пункта и пар
                 "параметр погоды — прогноз по параметру". Если прогноз получить не удалось, указываются только названия
                 метеорологической службы и населённого пункта.
        """
        pass

    @abstractmethod
    def get_current_weather(self, locality: str) -> Forecast:
        """
        Запрашивает текущую погоду по API.
        :param locality: Населённый пункт, для которого определяется погода.
        :return: Текущая погода, состоящий из названий метеорологической службы, населённого пункта и пар
                 "параметр погоды — прогноз по параметру". Если погоду получить не удалось, указываются только названия
                 метеорологической службы и населённого пункта.
        """
        pass
