from copy import deepcopy

from django.contrib.auth.models import User
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions, status, serializers, viewsets
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from mockapi.models.cart_item import CartItem
from mockapi.models.customer import Customer
from mockapi.models.order import Order
from mockapi.models.order_item import OrderItem
from mockapi.models.product import Product
from mockapi.models.shop import Shop
from mockapi.models.statuses import OrderStatus, DeliveryStatus
from mockapi.models.wishlist_item import WishListItem
from mockapi.serializers import ProductSerializer, UserSerializer, \
    UserSerializerPost, UserSerializerDetails, UserSerializerUpdate, ShopSerializer, WishListSerializer, CartSerializer, \
    OrderStatusesSerializer, OrderSerializer, OrderDetailsSerializer
from mockapi.views import CustomPagination


class UserAPIList(generics.ListAPIView):
    serializer_class = UserSerializer
    pagination_class = CustomPagination
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return User.objects.all()


class UserAPICreate(generics.CreateAPIView):
    serializer_class = UserSerializerPost
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class UserAPIRetrieve(generics.RetrieveAPIView):
    serializer_class = UserSerializerDetails
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return User.objects.all()

    def get(self, request, *args, **kwargs):
        instance = User.objects.get(pk=kwargs['pk'])
        if instance.pk != request.user.pk:
            serializer = UserSerializerDetails(instance,
                                               exclude=['password',
                                                        'is_superuser',
                                                        'is_staff', 'is_active',
                                                        'groups',
                                                        'user_permissions'])
        else:
            serializer = UserSerializerDetails(instance)
        return Response(serializer.data)


class UserAPIUpdate(generics.UpdateAPIView):
    serializer_class = UserSerializerUpdate
    http_method_names = ['patch']
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.id).all()


class SearchParamsSerializer(serializers.Serializer):
    final_price__gte = serializers.IntegerField(required=False)
    final_price__lte = serializers.IntegerField(required=False)


class ProductAPIList(generics.ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = CustomPagination
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = Product.objects.all()
        search_params = self.request.GET

        for key, value in search_params.items():
            if key == 'page':
                continue
            queryset = queryset.filter(**{key: value})

        return queryset

    @swagger_auto_schema(query_serializer=SearchParamsSerializer)
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class ProductAPICreate(generics.CreateAPIView):
    serializer_class = ProductSerializer
    pagination_class = CustomPagination
    permission_classes = [permissions.IsAuthenticated]

    authentication_classes = [JWTAuthentication]


class ProductAPIDestroy(generics.DestroyAPIView):
    serializer_class = ProductSerializer
    http_method_names = ['delete']
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return Product.objects.all()


class ProductAPIRetrieve(generics.RetrieveAPIView):
    serializer_class = ProductSerializer
    http_method_names = ['get']
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Product.objects.all()


class ProductAPIUpdate(generics.UpdateAPIView):
    serializer_class = ProductSerializer
    http_method_names = ['patch']
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return Product.objects.all()


class ProductAPISearch(generics.GenericAPIView):
    serializer_class = ProductSerializer
    parser_classes = [JSONParser]
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Product.objects.all()

    def post(self, request, *args, **kwargs):
        search_params = request.data
        try:
            queryset = Product.objects.filter().all()
            for key, value in search_params.items():
                queryset = queryset.filter(**{key: value})
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)


class ShopAPIRetrieve(generics.RetrieveAPIView):
    serializer_class = ShopSerializer
    permission_classes = [permissions.AllowAny]
    http_method_names = ['get']

    def get_queryset(self):
        return Shop.objects.all()


class ShopAPIPatch(generics.UpdateAPIView):
    serializer_class = ShopSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['patch']
    lookup_field = 'pk'

    def get_queryset(self):
        return Shop.objects.all()

    @swagger_auto_schema(
        operation_description="Обновление магазина",
        responses={
            200: ShopSerializer,
            400: "Ошибка валидации",
            401: "Неавторизован",
            404: "Магазин не найден"
        }
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


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


class OrderStatusesAPIList(generics.ListAPIView):
    serializer_class = OrderStatusesSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return OrderStatus.objects.all()


class DeliveryStatusesAPIList(generics.ListAPIView):
    serializer_class = OrderStatusesSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return OrderStatus.objects.all()


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


class AdminProductAPIChangeQty(generics.UpdateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    #
    def get_queryset(self):
        return Product.objects.all()

    def patch(self, request, *args, **kwargs):

        product_id = request.data.get('product_id')
        is_increment = request.data.get('is_increment')

        product = None
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Товар не найден'}, status=status.HTTP_404_NOT_FOUND)

        if is_increment is False:
            if product.quantity == 0:
                return Response({'error': 'Не может быть товара меньше нуля!'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                product.quantity -= 1
                product.save()
        else:
            product.quantity += 1
            product.save()

        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderAPICreate(generics.CreateAPIView):
    serializer_class = OrderSerializer
    pagination_class = CustomPagination
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return Order.objects.filter(
            customer=Customer.objects.get(user=self.request.user))

    def post(self, request, *args, **kwargs):

        customer_id = request.user.id
        delivery_address = request.data.get('deliveryAddress')
        delivery_contact = request.data.get('deliveryContact')
        delivery_name = request.data.get('deliveryName')
        delivery_comment = request.data.get('deliveryComment')
        total_cost = request.data.get('totalPrice')
        is_paid = request.data.get('isOrderPaid')

        cart_items = CartItem.objects.filter(
            customer=Customer.objects.get(user=self.request.user))

        new_order = Order(
            customer_id=customer_id,
            order_status=OrderStatus.objects.get(pk=1),
            delivery_status=DeliveryStatus.objects.get(pk=1),
            delivery_address=delivery_address,
            delivery_contact=delivery_contact,
            delivery_name=delivery_name,
            delivery_comment=delivery_comment,
            total_cost=total_cost,
            is_paid=is_paid,
        )

        new_order_items = []
        for item in cart_items:
            item_qty = item.qty
            product = Product.objects.get(id=item.product_id)
            product_qty = product.quantity
            diff = product_qty - item_qty
            if diff < 0:
                return Response({'error': f'Товара {product.title} не достаточно на складе!'},
                                status=status.HTTP_400_BAD_REQUEST)
            new_order_item = OrderItem(
                product=product,
                order=new_order,
                qty=item_qty,
                black_price=product.black_price,
                final_price=product.final_price,
                total_cost=product.final_price * item_qty
            )
            new_order_items.append([product, new_order_item, item_qty])

        new_order.save()

        for item in new_order_items:
            item[0].quantity -= item[2]
            item[0].save()
            item[1].save()

        if is_paid is True:
            shop = Shop.objects.get(id=1)
            shop.balance += new_order.total_cost
            shop.save()

        for item in cart_items:
            item.delete()

        serializer = OrderSerializer(new_order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OrdersAPIList(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(
            customer=Customer.objects.get(user=user))


class OrdersAdminAPIList(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return Order.objects.all()
        return Order.objects.filter(
            customer=Customer.objects.get(user=user))


class OrderAPIDetails(generics.RetrieveAPIView):
    serializer_class = OrderDetailsSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    http_method_names = ['get']

    def get_serializer_context(self):
        return {'request': self.request, 'format': self.format_kwarg, 'view': self}

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return Order.objects.all()
        return Order.objects.filter(
            customer=Customer.objects.get(user=self.request.user))
