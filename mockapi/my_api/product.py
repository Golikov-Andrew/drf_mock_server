from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions, status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from mockapi.my_api.common import SearchParamsSerializer
from mockapi.models.product import Product
from mockapi.my_serializers.other import ProductSerializer
from mockapi.views import CustomPagination


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
