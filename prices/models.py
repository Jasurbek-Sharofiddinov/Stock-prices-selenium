from django.db import models


class AluminiumPrice(models.Model):
    aluminium_price = models.CharField(max_length=255)
    last_time = models.DateTimeField(auto_now=True)


class PVCPrice(models.Model):
    pvc_futures_price = models.CharField(max_length=255)
    last_time = models.DateTimeField(auto_now=True)
