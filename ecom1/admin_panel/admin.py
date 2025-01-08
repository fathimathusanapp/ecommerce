from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser  # Import your model

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'Address')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'Address')
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('Address',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('Address',)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
