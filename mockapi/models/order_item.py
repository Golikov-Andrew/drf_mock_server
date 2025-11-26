from django.db import models

from mockapi.models.order import Order
from mockapi.models.product import Product


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    qty = models.IntegerField(default=1)
    black_price = models.FloatField(blank=False)
    final_price = models.FloatField(blank=False)
    total_cost = models.FloatField(blank=False)

