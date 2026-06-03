from django.urls import path
from .views import barang_masuk, barang_keluar, transaksi_list

urlpatterns = [
    path('', transaksi_list, name='transaksi_list'),
    path('masuk/', barang_masuk, name='barang_masuk'),
    path('keluar/', barang_keluar, name='barang_keluar'),
]