from django.urls import path

import mockapi.my_api.cart
import mockapi.my_api.common
import mockapi.my_api.order
import mockapi.my_api.product
import mockapi.my_api.user
import mockapi.my_api.wishlist
from mockapi import api
from mockapi.views import index, DecoratedTokenObtainPairView, \
    DecoratedTokenRefreshView, CustomTokenObtainPairView

urlpatterns = [
    path('', index, name='homepage'),
    path('token/', CustomTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('token/refresh/', DecoratedTokenRefreshView.as_view(),
         name='token_refresh'),

    path('user/by-token/', mockapi.my_api.user.UserAPIGetByToken.as_view(),
         name='api_user_get_by_token'),

    path('users/', mockapi.my_api.user.UserAPIList.as_view(),
         name='api_users_list'),
    path('users/register/', mockapi.my_api.user.UserAPICreate.as_view(),
         name='api_users_create'),
    path('users/details/<int:pk>/', mockapi.my_api.user.UserAPIRetrieve.as_view(),
         name='api_users_retrieve'),
    path('users/update/<int:pk>/', mockapi.my_api.user.UserAPIUpdate.as_view(),
         name='api_users_update'),

    path('products/', mockapi.my_api.product.ProductAPIList.as_view(),
         name='api_products_list'),
    path('products/', mockapi.my_api.product.ProductAPICreate.as_view(),
         name='api_products_create'),
    path('products/details/<int:pk>/', mockapi.my_api.product.ProductAPIRetrieve.as_view(),
         name='api_products_details'),
    path('products/update/<int:pk>/', mockapi.my_api.product.ProductAPIUpdate.as_view(),
         name='api_products_patch'),
    path('products/delete/<int:pk>/', mockapi.my_api.product.ProductAPIDestroy.as_view(),
         name='api_products_delete'),
    path('products/search/', mockapi.my_api.product.ProductAPISearch.as_view(),
         name='api_products_search'),

    path('shop/details/<int:pk>/', mockapi.my_api.common.ShopAPIRetrieve.as_view(),
         name='shop_details'),
    path('shop/<int:pk>/', mockapi.my_api.common.ShopAPIPatch.as_view(),
         name='shop_patch'),

    path('wishlist/', mockapi.my_api.wishlist.WishListAPIList.as_view(),
         name='wishlist_list'),
    path('wishlist/add/', mockapi.my_api.wishlist.WishListAPICreate.as_view(),
         name='wishlist_add'),
    path('wishlist/remove/<int:product_id>/', mockapi.my_api.wishlist.WishListAPIDestroy.as_view(),
         name='wishlist_remove'),

    path('cart/', mockapi.my_api.cart.CartAPIList.as_view(),
         name='cart_list'),
    path('cart/product/add/', mockapi.my_api.cart.CartAPIAddProduct.as_view(),
         name='cart_product_add'),
    path('cart/product/remove/<int:product_id>/', mockapi.my_api.cart.CartAPIRemoveProduct.as_view(),
         name='cart_product_remove'),

    path('order_statuses/', mockapi.my_api.order.OrderStatusesAPIList.as_view(),
         name='order_statuses_list'),
    path('delivery_statuses/', mockapi.my_api.order.DeliveryStatusesAPIList.as_view(),
         name='delivery_statuses_list'),

    path('cart/product/change-qty/', mockapi.my_api.cart.CartAPIChangeQtyItem.as_view(),
         name='cart_product_change_qty'),
    path('shop-admin/product/change-qty/', mockapi.my_api.product.AdminProductAPIChangeQty.as_view(),
         name='admin_product_change_qty'),

    path('order/create/', mockapi.my_api.order.OrderAPICreate.as_view(), name="order_create"),
    path('order/update/', mockapi.my_api.order.OrderAPIUpdate.as_view(), name="order_update"),
    path('orders/list/', mockapi.my_api.order.OrdersAPIList.as_view(), name="orders_list"),
    path('shop-admin/orders/list/', mockapi.my_api.order.OrdersAdminAPIList.as_view(), name="admin_orders_list"),
    path('order/details/<int:pk>/', mockapi.my_api.order.OrderAPIDetails.as_view(), name="order_details")

]
