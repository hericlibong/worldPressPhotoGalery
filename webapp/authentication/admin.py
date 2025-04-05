from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser',)
    list_filter = ('is_staff', 'is_superuser', 'groups',)
    search_fields = ('username', 'email', 'first_name', 'last_name',)
    fieldsets = (
        (None, {'fields': ('username', 'password',)}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions',)}),
        ('Important dates', {'fields': ('last_login', 'date_joined',)}),
    )


admin.site.register(User, CustomUserAdmin)
