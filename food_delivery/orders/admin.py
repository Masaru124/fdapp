from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff', 'is_customer')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('email',)
    
    # Add these required fields for UserAdmin
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username', 'first_name', 'last_name', 'phone_number', 'address')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_customer', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

admin.site.register(User, CustomUserAdmin)

# Customize admin site
admin.site.site_header = 'Pizza Delivery Administration'
admin.site.site_title = 'Pizza Delivery Admin Portal'
admin.site.index_title = 'Welcome to Pizza Delivery Admin Portal'
