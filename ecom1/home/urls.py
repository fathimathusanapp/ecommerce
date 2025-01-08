from django.urls import path
from . import views

app_name = 'home'


urlpatterns = [
    path('', views.index, name='index'),
    path('category/<int:category_id>/', views.product_view, name='product_view'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/update/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:product_id>/<str:action>/', views.update_cart_quantity, name='update_cart_quantity'),
    path('apply-coupon/', views.apply_coupon, name='apply_coupon'),
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('wishlist/remove_from_wishlist/<int:item_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('wishlist/move_to_cart/<int:item_id>/', views.move_to_cart, name='move_to_cart'),
    path('wishlist/move_to_cart/<int:item_id>/', views.move_to_cart, name='move_to_cart'),
    path('search/', views.search, name='search'), 
]
