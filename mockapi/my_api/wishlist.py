from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from mockapi.models.customer import Customer
from mockapi.models.product import Product
from mockapi.models.wishlist_item import WishListItem
from mockapi.my_serializers.other import WishListSerializer


class WishListAPIList(generics.ListAPIView):
    serializer_class = WishListSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_serializer_context(self):
        return {'request': self.request, 'format': self.format_kwarg, 'view': self}

    def get_queryset(self):
        return WishListItem.objects.filter(
            customer=Customer.objects.get(user=self.request.user))


class WishListAPICreate(generics.CreateAPIView):
    serializer_class = WishListSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_serializer_context(self):
        return {'request': self.request, 'format': self.format_kwarg, 'view': self}

    #
    def get_queryset(self):
        return WishListItem.objects.filter(
            customer=Customer.objects.get(user=self.request.user))

    def post(self, request, *args, **kwargs):

        product_id = request.data.get('product_id')
        customer_id = request.user.id

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Товар не найден'}, status=status.HTTP_404_NOT_FOUND)

        wishlist_item = WishListItem.objects.filter(
            customer_id=customer_id,
            product_id=product_id
        ).first()

        if wishlist_item:
            return Response({'error': 'Товар уже в вишлисте'}, status=status.HTTP_400_BAD_REQUEST)

        wishlist_item = WishListItem.objects.create(
            customer_id=customer_id,
            product=product
        )

        serializer = WishListSerializer(wishlist_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class WishListAPIDestroy(generics.DestroyAPIView):
    serializer_class = WishListSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    #
    def get_queryset(self):
        return WishListItem.objects.filter(
            customer=Customer.objects.get(user=self.request.user))

    def delete(self, request, *args, **kwargs):

        product_id = kwargs.get('product_id')
        customer_id = request.user.id

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Товар не найден'}, status=status.HTTP_404_NOT_FOUND)

        wishlist_item = WishListItem.objects.filter(
            customer_id=customer_id,
            product_id=product_id
        ).first()

        if not wishlist_item:
            return Response({'error': 'Товара нет в вишлисте'}, status=status.HTTP_400_BAD_REQUEST)

        wishlist_item.delete()

        return Response(
            {'message': 'Товар успешно удалён из вишлиста'},
            status=status.HTTP_204_NO_CONTENT
        )
