from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers, generics, permissions

from mockapi.models.shop import Shop
from mockapi.my_serializers.other import ShopSerializer


class SearchParamsSerializer(serializers.Serializer):
    final_price__gte = serializers.IntegerField(required=False)
    final_price__lte = serializers.IntegerField(required=False)


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
