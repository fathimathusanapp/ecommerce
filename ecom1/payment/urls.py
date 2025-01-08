from django.urls import path
from . import views  # Import views properly

app_name = 'payment'

urlpatterns = [
    path('checkout/', views.checkout_view, name='checkout'),
    path('payment-method/', views.payment_method, name='payment_method'),
    path('payment-success/<int:order_id>/', views.payment_success, name='payment_success'),
    path('payment-fail/', views.payment_fail, name='payment_fail'),

    path('order/', views.order, name='order'),
    path('order/confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),

    path('change-order-status/<int:pid>/', views.change_order_status, name='change_order_status'),
]
