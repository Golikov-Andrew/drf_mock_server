from django.urls import path

from mockapi import api
from mockapi.views import index, DecoratedTokenObtainPairView, \
    DecoratedTokenRefreshView, CustomTokenObtainPairView

urlpatterns = [
    path('', index, name='homepage'),
    path('token/', CustomTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('token/refresh/', DecoratedTokenRefreshView.as_view(),
         name='token_refresh'),

    path('users/', api.UserAPIList.as_view(),
         name='api_users_list'),
    path('users/register/', api.UserAPICreate.as_view(),
         name='api_users_create'),
    path('users/details/<int:pk>/', api.UserAPIRetrieve.as_view(),
         name='api_users_retrieve'),
    path('users/update/<int:pk>/', api.UserAPIUpdate.as_view(),
         name='api_users_update'),

    path('products/', api.ProductAPIList.as_view(),
         name='api_products_list'),
    path('products/', api.ProductAPICreate.as_view(),
         name='api_products_create'),
    path('products/details/<int:pk>/', api.ProductAPIRetrieve.as_view(),
         name='api_products_details'),
    path('products/update/<int:pk>/', api.ProductAPIUpdate.as_view(),
         name='api_products_patch'),
    path('products/delete/<int:pk>/', api.ProductAPIDestroy.as_view(),
         name='api_products_delete'),
    path('products/search/', api.ProductAPISearch.as_view(),
         name='api_products_search'),

    path('shop/details/<int:pk>/', api.ShopAPIRetrieve.as_view(),
         name='shop_details'),
    path('shop/<int:pk>/', api.ShopAPIPatch.as_view(),
         name='shop_patch'),

    path('wishlist/', api.WishListAPIList.as_view(),
         name='wishlist_list'),
    path('wishlist/add/', api.WishListAPICreate.as_view(),
         name='wishlist_add'),
    path('wishlist/remove/<int:product_id>/', api.WishListAPIDestroy.as_view(),
         name='wishlist_remove'),

]
