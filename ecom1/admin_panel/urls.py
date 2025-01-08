from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),  # Default view when accessing /adminpanel/
    path('user_management/', views.user_management, name='user_management'),
    path('activate-user/<int:user_id>/', views.activate_user, name='activate_user'),
    path('deactivate-user/<int:user_id>/', views.deactivate_user, name='deactivate_user'),
    path('logout/', views.logout_view, name='logout'),

    path('productdashboard/', views.product_dashboard, name='product_dashboard'),
    path('productdashboard/add/', views.add_product, name='add_product'),
    path('productdashboard/edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('productdashboard/delete/<int:product_id>/', views.delete_product, name='delete_product'),

    path('categories/', views.category_list, name='category_list'),
    path('categories/add/', views.add_category, name='add_category'),
    path('categories/edit/<int:pk>/', views.edit_category, name='edit_category'),
    path('categories/delete/<int:pk>/', views.delete_category, name='delete_category'),

    path('coupons/', views.coupon_list, name='coupon_list'),
    path('add-coupon/', views.add_coupon, name='add_coupon'),
    path('edit-coupon/<int:coupon_id>/', views.edit_coupon, name='edit_coupon'),
    path('delete-coupon/<int:coupon_id>/', views.delete_coupon, name='delete_coupon'),
 
    path('orders/', views.admin_order, name='admin_order'),
    path('update-order-status/', views.admin_update_order_status, name='admin_update_order_status'),

    path('carousel/', views.carousel_list, name='carousel_list'),
    path('carousel/add/', views.add_carousel, name='add_carousel'),
    path('carousel/edit/<int:pk>/', views.edit_carousel, name='edit_carousel'),
    path('carousel/delete/<int:pk>/', views.delete_carousel, name='delete_carousel'),
    
]
