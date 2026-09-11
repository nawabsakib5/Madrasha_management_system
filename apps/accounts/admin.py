from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'full_name', 'role', 'email', 'is_active')
    list_filter = ('role', 'is_active', 'is_staff')
    search_fields = ('username', 'full_name', 'email')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('full_name', 'email', 'phone', 'profile_picture')}),
        ('Role & Permissions', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Security', {'fields': ('must_change_password', 'two_factor_enabled')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'full_name', 'role', 'password1', 'password2'),
        }),
    )

    ordering = ('username',)