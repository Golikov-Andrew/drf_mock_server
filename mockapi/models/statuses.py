from django.db import models


class OrderStatus(models.Model):
    title = models.TextField()


class DeliveryStatus(models.Model):
    title = models.TextField()
