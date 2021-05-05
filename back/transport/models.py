from django.db import models

class Station(models.Model):
    station = models.CharField(blank=False, null=True, max_length=500)
    network = models.CharField(blank=False, null=True, max_length=500)
    lat = models.FloatField(blank=False, null=True)
    lon = models.FloatField(blank=False, null=True)
    id_station = models.CharField(blank=False, null=True, max_length=50)
    class Meta:
        db_table = "Station"
