from django.urls import path
from . import views

app_name = 'produk'

urlpatterns = [
    path('', views.produk_list, name='list'),
    path('tambah/', views.tambah_produk, name='tambah'),
    path('edit/<int:id>/', views.produk_edit, name='edit'),
    path('nonaktif/<int:id>/', views.produk_nonaktif, name='nonaktif'),
    path('aktifkan/<int:id>/', views.produk_aktifkan, name='aktifkan'),
]
