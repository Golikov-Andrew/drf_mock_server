from django.db import models

from mockapi.models.customer import Customer
from mockapi.models.statuses import OrderStatus, DeliveryStatus


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
    order_status = models.ForeignKey(OrderStatus, on_delete=models.SET_NULL)
    delivery_status = models.ForeignKey(DeliveryStatus, on_delete=models.SET_NULL)
    total_cost = models.FloatField(default=0)
    delivery_address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_paid = models.BooleanField(default=False)
