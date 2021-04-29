from django.db import models

class Station(models.Model):
    station = models.CharField(blank=False, null=True, max_length=500)
    network = models.CharField(blank=False, null=True, max_length=500)
    station_type = models.CharField(blank=False, null=True, max_length=500)
    lines = models.CharField(blank=False, null=True, max_length=500)
    station_ids = models.CharField(blank=False, null=True, max_length=500)

    class Meta:
        db_table = "Station"
