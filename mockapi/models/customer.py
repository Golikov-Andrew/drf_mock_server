from django.contrib.auth.models import User
from django.db import models

from mockapi.models.product import Product


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer')
    wishlist = models.ManyToManyField(Product, through='WishListItem', related_name='wishlists')

    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'
