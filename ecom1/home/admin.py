from django.contrib import admin
from .models import Category, Product, Cart , Coupon  
from payment.models import Order, OrderLine, Checkout
from .models import Carousel

# Category Admin
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category_image']
    search_fields = ['name']

# Product Admin
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'image', 'get_description']
    list_filter = ['category']
    search_fields = ['name', 'description']

# Cart Admin
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'quantity']
    search_fields = ['user__username', 'product__name']

# Order Admin
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'order_date', 'shipping_address', 'total_price', 'is_paid']
    list_filter = ['order_date', 'is_paid']
    search_fields = ['user__username', 'shipping_address']

# OrderLine Admin
@admin.register(OrderLine)
class OrderLineAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'unit_price', 'get_total']
    search_fields = ['order__id', 'product__name']

@admin.register(Checkout)
class CheckoutAdmin(admin.ModelAdmin):
    list_display = ['user', 'order', 'billing_address', 'shipping_address', 'total_amount', 'payment_status', 'checkout_date']
    list_filter = ['payment_status', 'checkout_date']
    search_fields = ['user__username', 'order__id']

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_percentage', 'active')

@admin.register(Carousel)
class CarouselAdmin(admin.ModelAdmin):
    list_display = ('title', 'active')