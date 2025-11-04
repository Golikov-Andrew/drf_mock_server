from django.contrib.auth.models import User
from django.db import models


class Customer(models.Model):
    # limit_items_per_page = models.IntegerField(default=5)
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING,
                                 related_name='customer')


    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'