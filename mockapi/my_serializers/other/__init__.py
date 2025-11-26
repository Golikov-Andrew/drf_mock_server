from rest_framework import serializers

from mockapi.models.cart_item import CartItem
from mockapi.models.product import Product
from mockapi.models.shop import Shop
from mockapi.models.wishlist_item import WishListItem
from mockapi.my_serializers.common import DefaultValueSerializerMixin


class ProductSerializer(DefaultValueSerializerMixin,
                        serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    def get_image_url(self, obj):
        request = self.context.get('request')

        if obj.image_url:
            if request:
                return request.build_absolute_uri(obj.image_url.url)
            else:
                return obj.image_url.url

        return None

    class Meta:
        model = Product

        fields = '__all__'


class ShopSerializer(DefaultValueSerializerMixin,
                     serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = '__all__'


class WishListSerializer(DefaultValueSerializerMixin,
                         serializers.ModelSerializer):
    product = serializers.SerializerMethodField()

    def get_product(self, obj):
        serializer = ProductSerializer(obj.product, context=self.context)
        return serializer.data

    class Meta:
        model = WishListItem
        fields = ['product']


class CartSerializer(DefaultValueSerializerMixin,
                     serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ['product', 'qty']
