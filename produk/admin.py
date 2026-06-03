from django.contrib import admin
from .models import Produk

@admin.register(Produk)
class ProdukAdmin(admin.ModelAdmin):
    list_display = (
        'kode_produk',
        'nama_produk',
        'kategori',
        'stok',
        'stok_minimum',
        'is_active'
    )
    list_filter = ('kategori', 'is_active')
    search_fields = ('kode_produk', 'nama_produk')
