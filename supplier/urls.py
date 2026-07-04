from django.urls import path
from . import views

app_name = 'supplier'

urlpatterns = [
    path('', views.supplier_list, name='list'),
    path('tambah/', views.supplier_tambah, name='tambah'),
    path('edit/<int:id>/', views.supplier_edit, name='edit'),
    path('hapus/<int:id>/', views.supplier_hapus, name='hapus'),
]
