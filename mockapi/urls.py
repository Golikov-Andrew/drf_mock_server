from django.urls import path

from mockapi import api
from mockapi.views import index, DecoratedTokenObtainPairView, \
    DecoratedTokenRefreshView


urlpatterns = [
    path('', index, name='homepage'),
    path('token/', DecoratedTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('token/refresh/', DecoratedTokenRefreshView.as_view(),
         name='token_refresh'),

    path('users/', api.UserAPIList.as_view(),
         name='api_users_list'),
    path('users/create/', api.UserAPICreate.as_view(),
         name='api_users_create'),
    path('users/details/<int:pk>/', api.UserAPIRetrieve.as_view(),
         name='api_users_retrieve'),
    path('users/update/<int:pk>/', api.UserAPIUpdate.as_view(),
         name='api_users_update'),

    path('products/', api.ProductAPIListCreate.as_view(),
         name='api_products_list_create'),
    path('products/<int:pk>/', api.ProductAPIRetrieveUpdateDestroy.as_view(),
         name='api_products_retrieve_update-destroy'),
    path('products/search/', api.ProductAPISearch.as_view(),
         name='api_products_search'),

]
