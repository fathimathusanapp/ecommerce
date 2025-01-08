from django.contrib import admin
from .models import OTP, Address

class OTPAdmin(admin.ModelAdmin):
    list_display = ('user', 'otp_code', 'created_at')

class AddressAdmin(admin.ModelAdmin):
    list_display = ('user','first_name', 'last_name','phone_number', 'housename', 'street', 'city', 'state', 'zipcode')


admin.site.register(OTP, OTPAdmin)
admin.site.register(Address, AddressAdmin)
