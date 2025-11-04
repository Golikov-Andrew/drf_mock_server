from django.contrib.auth.models import User
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions, status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from mockapi.models.product import Product
from mockapi.serializers import ProductSerializer, UserSerializer, \
    UserSerializerPost, UserSerializerDetails, UserSerializerUpdate
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
        # return User.objects.filter(pk=self.kwargs['id']).all()
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


# tags_schema = openapi.Schema(
#     type=openapi.TYPE_ARRAY,
#     items=openapi.Schema(
#         type=openapi.TYPE_INTEGER,
#         format=openapi.FORMAT_INT32
#     ),
#     description='Список ID тегов',
#     example=[1, 2, 3]
# )


class ProductAPIListCreate(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    pagination_class = CustomPagination
    permission_classes = [permissions.AllowAny]

    # authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return Product.objects.all()

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        response['Access-Control-Allow-Origin'] = 'http://localhost:5173'
        response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
        response[
            'Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response


class ProductAPIRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    http_method_names = ['get', 'patch', 'delete']
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return Product.objects.all()


class ProductAPISearch(generics.GenericAPIView):
    serializer_class = ProductSerializer
    parser_classes = [JSONParser]
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return Product.objects.all()

    # @swagger_auto_schema(
    #     request_body=openapi.Schema(
    #         type=openapi.TYPE_OBJECT,
    #         properties={
    #             'title': openapi.Schema(type=openapi.TYPE_STRING,
    #                                     description='Точный заголовок'),
    #             'title__icontains': openapi.Schema(type=openapi.TYPE_STRING,
    #                                                description='Подстрока заголовка'),
    #             'content__icontains': openapi.Schema(
    #                 type=openapi.TYPE_STRING,
    #                 description='Подстрока описания'),
    #             'is_done': openapi.Schema(type=openapi.TYPE_BOOLEAN,
    #                                       description='Статус Выполнена'),
    #             'project': openapi.Schema(type=openapi.TYPE_INTEGER,
    #                                       description='Проект'),
    #             'created_at': openapi.Schema(type=openapi.TYPE_STRING,
    #                                          format=openapi.FORMAT_DATETIME,
    #                                          description='Дата-время создания'),
    #             'created_at__gte': openapi.Schema(type=openapi.TYPE_STRING,
    #                                               format=openapi.FORMAT_DATETIME,
    #                                               description='Дата-время создания (после)'),
    #             'created_at__lte': openapi.Schema(type=openapi.TYPE_STRING,
    #                                               format=openapi.FORMAT_DATETIME,
    #                                               description='Дата-время создания (до)'),
    #             'begin_at': openapi.Schema(type=openapi.TYPE_STRING,
    #                                        format=openapi.FORMAT_DATETIME,
    #                                        description='Дата-время начала'),
    #             'begin_at__gte': openapi.Schema(type=openapi.TYPE_STRING,
    #                                             format=openapi.FORMAT_DATETIME,
    #                                             description='Дата-время начала (после)'),
    #             'begin_at__lte': openapi.Schema(type=openapi.TYPE_STRING,
    #                                             format=openapi.FORMAT_DATETIME,
    #                                             description='Дата-время начала (до)'),
    #             'duration__gte': openapi.Schema(type=openapi.TYPE_INTEGER,
    #                                             description='Продолжительность >= (в секундах)'),
    #             'duration__lte': openapi.Schema(type=openapi.TYPE_INTEGER,
    #                                             description='Продолжительность <= (в секундах)'),
    #             'tags__in': tags_schema
    #
    #         },
    #         # required=['title'],
    #     ),
    #     responses={
    #         200: openapi.Response('Успешный поиск',
    #                               ProjectSerializer(many=True)),
    #         400: 'Неверный формат запроса'
    #     }
    # )
    def post(self, request, *args, **kwargs):
        search_params = request.data
        try:
            queryset = Product.objects.filter(
                owner_id=self.request.user.id).all()
            for key, value in search_params.items():
                queryset = queryset.filter(**{key: value})
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)

# class ProjectAPIListCreate(generics.ListCreateAPIView):
#     serializer_class = ProjectSerializer
#     pagination_class = CustomPagination
#     permission_classes = [permissions.IsAuthenticated]
#     authentication_classes = [JWTAuthentication]
#
#     def get_queryset(self):
#         return Project.objects.filter(owner_id=self.request.user.id).all()
#
#
# class ProjectAPIRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
#     serializer_class = ProjectSerializer
#     http_method_names = ['get', 'patch', 'delete']
#     permission_classes = [permissions.IsAuthenticated]
#     authentication_classes = [JWTAuthentication]
#
#     def get_queryset(self):
#         return Project.objects.filter(owner_id=self.request.user.id).all()
#
#
# class ProjectAPISearch(generics.GenericAPIView):
#     serializer_class = ProjectSerializer
#     parser_classes = [JSONParser]
#     permission_classes = [permissions.IsAuthenticated]
#     authentication_classes = [JWTAuthentication]
#
#     def get_queryset(self):
#         return Project.objects.filter(owner_id=self.request.user.id).all()
#
#     @swagger_auto_schema(
#         request_body=openapi.Schema(
#             type=openapi.TYPE_OBJECT,
#             properties={
#                 'title': openapi.Schema(type=openapi.TYPE_STRING,
#                                         description='Точный заголовок'),
#                 'title__icontains': openapi.Schema(type=openapi.TYPE_STRING,
#                                                    description='Подстрока заголовка'),
#                 'description__icontains': openapi.Schema(
#                     type=openapi.TYPE_STRING,
#                     description='Подстрока описания'),
#                 'color': openapi.Schema(type=openapi.TYPE_STRING,
#                                         description='Цвет в формате #RRGGBB (HEX)'),
#                 'created_at': openapi.Schema(type=openapi.TYPE_STRING,
#                                              format=openapi.FORMAT_DATETIME,
#                                              description='Дата-время создания'),
#                 'created_at__gte': openapi.Schema(type=openapi.TYPE_STRING,
#                                                   format=openapi.FORMAT_DATETIME,
#                                                   description='Дата-время создания (после)'),
#                 'created_at__lte': openapi.Schema(type=openapi.TYPE_STRING,
#                                                   format=openapi.FORMAT_DATETIME,
#                                                   description='Дата-время создания (до)'),
#                 'tags__in': tags_schema
#
#             },
#             # required=['title'],
#         ),
#         responses={
#             200: openapi.Response('Успешный поиск',
#                                   ProjectSerializer(many=True)),
#             400: 'Неверный формат запроса'
#         }
#     )
#     def post(self, request, *args, **kwargs):
#         search_params = request.data
#         try:
#             queryset = Project.objects.filter(
#                 owner_id=self.request.user.id).all()
#             for key, value in search_params.items():
#                 queryset = queryset.filter(**{key: value})
#             serializer = self.get_serializer(queryset, many=True)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({'error': str(e)},
#                             status=status.HTTP_400_BAD_REQUEST)
#
#
# class TagAPIListCreate(generics.ListCreateAPIView):
#     serializer_class = TagSerializer
#     pagination_class = CustomPagination
#     permission_classes = [permissions.IsAuthenticated]
#     authentication_classes = [JWTAuthentication]
#
#     def get_queryset(self):
#         return Tag.objects.filter(owner_id=self.request.user.id).all()
#
#
# class TagAPIRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
#     serializer_class = TagSerializer
#     http_method_names = ['get', 'patch', 'delete']
#     permission_classes = [permissions.IsAuthenticated]
#     authentication_classes = [JWTAuthentication]
#
#     def get_queryset(self):
#         return Tag.objects.filter(owner_id=self.request.user.id).all()
#
#
# class TagAPISearch(generics.GenericAPIView):
#     serializer_class = TagSerializer
#     filterset_class = TagFilter
#     parser_classes = [JSONParser]
#     permission_classes = [permissions.IsAuthenticated]
#     authentication_classes = [JWTAuthentication]
#
#     def get_queryset(self):
#         return Tag.objects.filter(owner_id=self.request.user.id).all()
#
#     @swagger_auto_schema(
#         request_body=openapi.Schema(
#             type=openapi.TYPE_OBJECT,
#             properties={
#                 'title': openapi.Schema(type=openapi.TYPE_STRING,
#                                         description='Точный заголовок'),
#                 'title__icontains': openapi.Schema(type=openapi.TYPE_STRING,
#                                                    description='Подстрока заголовка'),
#                 'color': openapi.Schema(type=openapi.TYPE_STRING,
#                                         description='Цвет в формате #RRGGBB (HEX)'),
#                 'created_at': openapi.Schema(type=openapi.TYPE_STRING,
#                                              format=openapi.FORMAT_DATETIME,
#                                              description='Дата-время создания'),
#                 'created_at__gte': openapi.Schema(type=openapi.TYPE_STRING,
#                                                   format=openapi.FORMAT_DATETIME,
#                                                   description='Дата-время создания (после)'),
#                 'created_at__lte': openapi.Schema(type=openapi.TYPE_STRING,
#                                                   format=openapi.FORMAT_DATETIME,
#                                                   description='Дата-время создания (до)'),
#
#             },
#             # required=['title'],
#         ),
#         responses={
#             200: openapi.Response('Успешный поиск', TagSerializer(many=True)),
#             400: 'Неверный формат запроса'
#         }
#     )
#     def post(self, request, *args, **kwargs):
#         search_params = request.data
#         try:
#             queryset = Tag.objects.filter(owner_id=self.request.user.id).all()
#             for key, value in search_params.items():
#                 queryset = queryset.filter(**{key: value})
#             serializer = self.get_serializer(queryset, many=True)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({'error': str(e)},
#                             status=status.HTTP_400_BAD_REQUEST)
