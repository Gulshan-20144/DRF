# user/admin.py

from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class CustomUserAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'contact', 'dob', 'gender')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2',  'contact', 'dob', 'gender','is_staff', 'is_superuser'),
        }),
    )
    list_display = ('id', 'password','email', 'first_name', 'last_name','contact', 'dob', 'gender','is_staff')
    search_fields = ('id', 'email', 'first_name', 'last_name')
    list_filter = ('email', 'first_name')
    ordering = ('id',)

admin.site.register(User, CustomUserAdmin)
