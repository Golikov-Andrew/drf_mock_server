from django.db import models

from mockapi.models.product import Product
from mockapi.models.shop import Shop


class ProductStockQty(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stock_qty')
    qty = models.IntegerField(default=0)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='products_stock')
