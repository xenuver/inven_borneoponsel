from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
 
 
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # Kolom yang tampil di daftar user
    list_display = ('username', 'email', 'get_full_name', 'role', 'is_active')
    list_filter  = ('role', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
 
    # Tambah field 'role' ke form edit user
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Role & Akses', {'fields': ('role',)}),
    )
 
    # Tambah field 'role' ke form tambah user baru
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Role & Akses', {'fields': ('role',)}),
    )
 