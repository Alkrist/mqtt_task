from django.db import models

class Coin(models.Model):
    identifier = models.CharField(max_length=64, null=True)
    rank = models.CharField(max_length=64, null=True)
    symbol = models.CharField(max_length=64, null=True)
    name = models.CharField(max_length=64, null=True)
    supply = models.CharField(max_length=255, null=True)
