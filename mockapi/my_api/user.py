from django.contrib.auth.models import User
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from mockapi.my_serializers.user import UserSerializer, UserSerializerDetails, UserSerializerPost, UserSerializerUpdate
from mockapi.views import CustomPagination


class UserAPIList(generics.ListAPIView):
    serializer_class = UserSerializer
    pagination_class = CustomPagination
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return User.objects.all()


class UserAPIGetByToken(generics.RetrieveAPIView):
    serializer_class = UserSerializerDetails
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return User.objects.all()

    def get(self, request, *args, **kwargs):
        user = request.user
        serialized = UserSerializerDetails(user,
                                           exclude=['password',
                                                    'is_superuser',
                                                    'is_staff', 'is_active',
                                                    'groups',
                                                    'user_permissions'])

        return Response(serialized.data)


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
