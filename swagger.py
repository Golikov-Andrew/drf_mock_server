from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from mockapi.generators import BothHttpAndHttpsSchemaGenerator

schema_view = get_schema_view(
    openapi.Info(
        title="GAVMOCK API",
        default_version='v1',
        description="Аутентификация, CRUD Юзеров и Продуктов",
        terms_of_service="https://www.example.com/policies",
        # contact=openapi.Contact(email="golikovandrew13@yandex.ru"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    patterns=[path('api/v1/', include('mockapi.urls')), ],
    # permission_classes=[permissions.IsAuthenticated],
    permission_classes=[permissions.AllowAny],
    generator_class=BothHttpAndHttpsSchemaGenerator

)
