from django.contrib import admin
from .models import Pelanggan


@admin.register(Pelanggan)
class PelangganAdmin(admin.ModelAdmin):
    list_display = ('nama', 'telepon', 'is_active', 'created_at')
    search_fields = ('nama', 'telepon')
