from django.contrib import admin
from .models import Transaksi, DetailTransaksi, LogStok, StokOpname

class DetailTransaksiInline(admin.TabularInline):
    model = DetailTransaksi
    extra = 1

@admin.register(Transaksi)
class TransaksiAdmin(admin.ModelAdmin):
    list_display = ('id', 'jenis_transaksi', 'tanggal', 'supplier', 'user')
    list_filter = ('jenis_transaksi',)
    inlines = [DetailTransaksiInline]

@admin.register(LogStok)
class LogStokAdmin(admin.ModelAdmin):
    list_display = (
        'produk',
        'perubahan',
        'stok_sebelum',
        'stok_sesudah',
        'tanggal'
    )
    list_filter = ('tanggal',)


@admin.register(StokOpname)
class StokOpnameAdmin(admin.ModelAdmin):
    list_display = ('produk', 'stok_sistem', 'stok_fisik', 'selisih', 'user', 'tanggal')
    list_filter = ('tanggal',)
