from django.utils.dateformat import DateFormat
from rest_framework import serializers

from mockapi.models.order import Order
from mockapi.models.order_item import OrderItem
from mockapi.models.shop import Shop
from mockapi.my_serializers.common import DefaultValueSerializerMixin
from mockapi.my_serializers.other import ProductSerializer


class OrderSerializer(DefaultValueSerializerMixin,
                      serializers.ModelSerializer):
    order_status_title = serializers.SerializerMethodField()
    delivery_status_title = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    def get_order_status_title(self, obj):
        if obj.order_status:
            return obj.order_status.title
        return None

    def get_delivery_status_title(self, obj):
        if obj.delivery_status:
            return obj.delivery_status.title
        return None

    def get_created_at(self, obj):
        if obj.created_at:
            return DateFormat(obj.created_at).format('Y-m-d H:i')
        return None

    def get_updated_at(self, obj):
        if obj.updated_at:
            return DateFormat(obj.updated_at).format('Y-m-d H:i')
        return None

    class Meta:
        model = Order
        fields = '__all__'


class OrderShopSerializer(OrderSerializer):
    shop_balance = serializers.SerializerMethodField()

    def get_shop_balance(self, obj):
        shop = Shop.objects.get(pk=1)
        return shop.balance


class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()

    def get_product(self, obj):
        serializer = ProductSerializer(obj.product, context=self.context)
        return serializer.data

    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderDetailsSerializer(OrderSerializer):
    order_items = serializers.SerializerMethodField()

    def get_order_items(self, obj):
        items = OrderItem.objects.filter(order=obj)
        return OrderItemSerializer(items, many=True, context=self.context).data

    class Meta:
        model = Order
        fields = '__all__'
