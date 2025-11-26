from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from mockapi.models.cart_item import CartItem
from mockapi.models.customer import Customer
from mockapi.models.order import Order
from mockapi.models.order_item import OrderItem
from mockapi.models.product import Product
from mockapi.models.shop import Shop
from mockapi.models.statuses import OrderStatus, DeliveryStatus
from mockapi.my_serializers.order import OrderSerializer, OrderDetailsSerializer, OrderShopSerializer
from mockapi.my_serializers.statuses import OrderStatusesSerializer
from mockapi.views import CustomPagination


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


class OrderAPIUpdate(generics.UpdateAPIView):
    serializer_class = OrderSerializer
    http_method_names = ['patch']
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return Order.objects.all()
        return Order.objects.filter(
            customer=Customer.objects.get(user=self.request.user))

    def patch(self, request, *args, **kwargs):
        order_id = request.data.get('order_id')
        attribute_name = request.data.get('attribute_name')
        attribute_value = request.data.get('attribute_value')

        order = None
        try:
            order = Order.objects.get(id=order_id)
        except Product.DoesNotExist:
            return Response({'error': 'Заказ не найден'}, status=status.HTTP_400_BAD_REQUEST)

        if attribute_name == 'order_status':
            order_statuses = OrderStatus.objects.values_list('title', flat=True)
            if attribute_value in order_statuses:
                order.order_status = OrderStatus.objects.get(title=attribute_value)
            else:
                return Response({'error': f'Нет такого значения {attribute_value} для атрибута {attribute_name}'},
                                status=status.HTTP_400_BAD_REQUEST)

        elif attribute_name == 'delivery_status':
            delivery_statuses = DeliveryStatus.objects.values_list('title', flat=True)
            if attribute_value in delivery_statuses:
                order.delivery_status = DeliveryStatus.objects.get(title=attribute_value)
            else:
                return Response({'error': f'Нет такого значения {attribute_value} для атрибута {attribute_name}'},
                                status=status.HTTP_400_BAD_REQUEST)

        elif attribute_name == 'is_paid':
            if isinstance(attribute_value, bool):
                order.is_paid = attribute_value
                shop = Shop.objects.get(pk=1)
                if attribute_value is True:
                    shop.balance += order.total_cost
                else:
                    shop.balance -= order.total_cost
                shop.save()
            else:
                return Response({'error': f'Значение {attribute_value} для атрибута {attribute_name} некорректное!'},
                                status=status.HTTP_400_BAD_REQUEST)

        order.save()
        serializer = OrderShopSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)


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
