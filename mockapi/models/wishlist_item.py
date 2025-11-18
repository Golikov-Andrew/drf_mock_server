from django.db import models

from mockapi.models.customer import Customer
from mockapi.models.product import Product


class WishListItem(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
