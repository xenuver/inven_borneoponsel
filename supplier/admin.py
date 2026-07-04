from django.contrib import admin
from .models import Supplier


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('nama_supplier', 'kontak_person', 'telepon', 'is_active')
    search_fields = ('nama_supplier', 'kontak_person')
