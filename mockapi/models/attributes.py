from django.db import models


class Color(models.Model):
    title = models.TextField()
    hex_value = models.TextField()


class Tag(models.Model):
    title = models.TextField()
    hex_value = models.TextField(default='#999999')
