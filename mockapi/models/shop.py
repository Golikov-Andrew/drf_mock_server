from django.db import models


class Shop(models.Model):
    title = models.CharField(max_length=150, default='Huawei')
    description = models.TextField(blank=True)
    balance = models.FloatField(default=0)
