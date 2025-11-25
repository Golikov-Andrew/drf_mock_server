from django.db import models

from mockapi.models.customer import Customer
from mockapi.models.product import Product


class CartItem(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, default=None)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # cart = models.ForeignKey(Customer, on_delete=models.CASCADE)
    qty = models.IntegerField(default=1)

