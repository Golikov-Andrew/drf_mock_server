from rest_framework import serializers

from mockapi.models.statuses import OrderStatus, DeliveryStatus
from mockapi.my_serializers.common import DefaultValueSerializerMixin


class OrderStatusesSerializer(DefaultValueSerializerMixin,
                              serializers.ModelSerializer):
    class Meta:
        model = OrderStatus
        fields = ['title']


class DeliveryStatusesSerializer(DefaultValueSerializerMixin,
                                 serializers.ModelSerializer):
    class Meta:
        model = DeliveryStatus
        fields = ['title']
