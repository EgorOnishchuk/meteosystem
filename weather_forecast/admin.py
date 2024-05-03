from django.contrib.admin import site
from .models import MeteorologicalService, MeteorologicalAPI

site.register(MeteorologicalService)
site.register(MeteorologicalAPI)
