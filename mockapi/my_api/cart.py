from copy import deepcopy

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from mockapi.models.cart_item import CartItem
from mockapi.models.customer import Customer
from mockapi.models.product import Product
from mockapi.my_serializers.other import CartSerializer


class CartAPIList(generics.ListAPIView):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return CartItem.objects.filter(
            customer=Customer.objects.get(user=self.request.user))


class CartAPIAddProduct(generics.CreateAPIView):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    #
    def get_queryset(self):
        return CartItem.objects.filter(
            customer=Customer.objects.get(user=self.request.user))

    def post(self, request, *args, **kwargs):

        product_id = request.data.get('product_id')
        customer_id = request.user.id

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Товар не найден'}, status=status.HTTP_404_NOT_FOUND)

        cart_item = CartItem.objects.filter(
            customer_id=customer_id,
            product_id=product_id
        ).first()

        if cart_item:
            return Response({'error': 'Товар уже в корзине'}, status=status.HTTP_400_BAD_REQUEST)

        cart_item = CartItem.objects.create(
            customer_id=customer_id,
            product=product
        )

        serializer = CartSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CartAPIRemoveProduct(generics.DestroyAPIView):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    #
    def get_queryset(self):
        return CartItem.objects.filter(
            customer=Customer.objects.get(user=self.request.user))

    def delete(self, request, *args, **kwargs):

        product_id = kwargs.get('product_id')
        customer_id = request.user.id

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Товар не найден'}, status=status.HTTP_404_NOT_FOUND)

        cart_item = CartItem.objects.filter(
            customer_id=customer_id,
            product_id=product_id
        ).first()

        if not cart_item:
            return Response({'error': 'Товара нет в корзине'}, status=status.HTTP_400_BAD_REQUEST)

        cart_item.delete()

        return Response(
            {'message': 'Товар успешно удалён из корзины'},
            status=status.HTTP_204_NO_CONTENT
        )


class CartAPIChangeQtyItem(generics.UpdateAPIView):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    #
    def get_queryset(self):
        return CartItem.objects.filter(
            customer=Customer.objects.get(user=self.request.user))

    def patch(self, request, *args, **kwargs):

        product_id = request.data.get('product_id')
        is_increment = request.data.get('is_increment')
        customer_id = request.user.id

        product = None
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Товар не найден'}, status=status.HTTP_404_NOT_FOUND)

        cart_item = CartItem.objects.filter(
            customer_id=customer_id,
            product_id=product_id
        ).first()

        if is_increment is True:
            if product.quantity <= 0:
                return Response({'error': 'Товара недостаточно на складе!'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                cart_item.qty += 1
                cart_item.save()
        else:
            if cart_item.qty - 1 <= 0:
                cart_item_deleted = deepcopy(cart_item)
                cart_item_deleted.qty = 0
                cart_item.delete()
                serializer = CartSerializer(cart_item_deleted)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                cart_item.qty -= 1
                cart_item.save()

        serializer = CartSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_200_OK)
