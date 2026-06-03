from django.urls import path
from . import views

app_name = 'kategori'

urlpatterns = [
    path('', views.kategori_list,   name='list'),
    path('tambah/', views.kategori_tambah, name='tambah'),
    path('edit/<int:id>/', views.kategori_edit,   name='edit'),
    path('hapus/<int:id>/', views.kategori_hapus,  name='hapus'),
]