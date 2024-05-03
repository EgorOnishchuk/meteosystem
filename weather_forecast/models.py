from django.db import models


class MeteorologicalProvider(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class MeteorologicalService(MeteorologicalProvider):
    description = models.TextField()
    link = models.CharField(max_length=50)


class MeteorologicalAPI(MeteorologicalProvider):
    url = models.CharField(max_length=200)
    key = models.CharField(max_length=200)
    meteorological_service = models.ForeignKey(
        'MeteorologicalService',
        on_delete=models.SET_NULL,
        null=True,
    )
