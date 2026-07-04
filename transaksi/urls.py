from django.urls import path
from .views import barang_masuk, barang_keluar, transaksi_list, stok_opname_list, stok_opname_simpan

urlpatterns = [
    path('', transaksi_list, name='transaksi_list'),
    path('masuk/', barang_masuk, name='barang_masuk'),
    path('keluar/', barang_keluar, name='barang_keluar'),
    path('stok-opname/', stok_opname_list, name='stok_opname_list'),
    path('stok-opname/simpan/', stok_opname_simpan, name='stok_opname_simpan'),
]